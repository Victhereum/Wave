from typing import Any

from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from wave.apps.payments.models import Payments
from wave.apps.payments.paginations import CustomPagination
from wave.apps.payments.serializers import PaymentSerializers
from wave.utils.choices import PaymentPlans
from wave.utils.custom_exceptions import CustomError
from wave.utils.payments import MoyasarAPIWrapper


class PaymentViewSet(ModelViewSet):
    serializer_class: PaymentSerializers = PaymentSerializers
    queryset = Payments.objects.all()
    pagination_class = CustomPagination
    payment = MoyasarAPIWrapper()
    lookup_field = "id"

    def month_number_to_text(self, month_number: int):
        months = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }

        return months.get(month_number, "Invalid Month")

    def get_serializer(self, *args: Any, **kwargs: Any) -> BaseSerializer:
        if self.action == "retrieve":
            return self.serializer_class.Fetch
        return self.serializer_class.Get

    def get_call_back(self):
        return f"{self.request.build_absolute_uri('/')}"

    def get_queryset(self) -> QuerySet:
        self.queryset = self.queryset.filter(user=self.request.user)
        if self.queryset.exists():
            return self.queryset
        raise CustomError.EmptyResponse()

    def get_object(self) -> Any:
        id = self.kwargs["id"]
        instance = get_object_or_404(Payments, id=id)
        self.check_object_permissions(self.request, instance)
        return instance

    @atomic
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = request.user
        serializer = PaymentSerializers.Create(data=request.data)
        if serializer.is_valid(raise_exception=True):
            amount = serializer.validated_data.get("amount", None)
            plan = serializer.validated_data.get("plan", None)
            currency = serializer.validated_data.get("currency", "SAR")
            month_text = self.month_number_to_text(month_number=int(datetime.now().date().month))
            plan_description = month_text if plan == PaymentPlans.MONTHLY else datetime.now().date().year
            description = f"Wave payment from {user.name} for {plan_description}"
            source = serializer.validated_data.pop("source", {})
            call_back = self.get_call_back()
            metadata = {"plan": plan}
            payment: dict = self.payment.create_payment(
                amount=amount,
                currency=currency,
                description=description,
                source=source,
                callback_url=call_back,
                metadata=metadata,
            )
            instance = Payments.objects.create(user=request.user, id=payment.get("id"))
            response = self.serializer_class.Get(instance=instance)
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        page = self.paginate_queryset(self.get_queryset())
        data = self.serializer_class.Get(instance=page, many=True).data
        return self.get_paginated_response(data)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        response = self.serializer_class.Fetch(instance)
        return Response(response.data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        raise PermissionDenied(detail="You can't update a record")

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        raise PermissionDenied(detail="You can't update a record")

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        raise PermissionDenied(detail="You can't delete a record")
