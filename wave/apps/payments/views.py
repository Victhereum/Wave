from typing import Any

from django.conf import settings
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
    """
    PaymentViewSet: Level Up Your Video Quest with Payment Magic

    Greetings, fellow adventurers of the VideoVerse! 🎮💰 Welcome to the realm of PaymentViewSet,
    where your heroic endeavors with videos are about to get a powerful upgrade. Gear up for an
    exhilarating journey as we blend the forces of videos and payments into one epic tale.

    The Chronicles Begin:
    Get ready to step into a world where videos meet payments in perfect harmony. PaymentViewSet
    emerges as your trusty guide, enhancing your VideoVerse experience like never before!

    Payment Sorcery:
    - create: Prepare to wield the ultimate spell to conjure payments that seamlessly integrate with
      your video conquests! ✨🧙‍♂️
      Magic Scroll: POST
      Command: /payments/create

      Quest Tips:
      Channel your inner spellcaster to define the amount and payment plan. Our payment wizards
      will craft a seamless journey, complete with callbacks that align with your heroic quest.

    - list: Embark on a treasure hunt that reveals the riches of your VideoVerse accomplishments,
      guarded by loyal pagination guardians! 🗺️📜
      Explorer's Scroll: GET
      Command: /payments

      Quest Tips:
      Journey through the scrolls guided by our wise pagination guardians. Uncover your hard-earned
      treasures in bite-sized portions, making your exploration smooth and delightful.

    - retrieve: Venture deeper into the realm as you unveil the secrets behind individual payments,
      adding a layer of mystique to your adventure! 🔍🤐
      Decoder Scroll: GET
      Command: /payments/{id}

      Quest Tips:
      Empower yourself to unravel the essence of a single payment. The response shall reveal the
      secrets you seek, letting you savor the thrill of discovery.

    Guardians of Forbidden Paths:
    Beware, brave seeker! Some paths are forbidden, guarded by formidable sentinels.
    - update and partial_update: These sacred records are untouchable, holding ancient power.
      Approach with respect. Forbidden: 403
    - destroy: The fabric of the realm shudders at the thought of deletion. Honor the balance and
      tread carefully. Forbidden: 403

    Trusty Allies:
    Meet your allies, the valiant serializers, standing by to help you navigate this grand quest.
    - PaymentSerializers.Get: Reveals the full scope of payment details.
    - PaymentSerializers.Fetch: Fetches essential payment information, offering a taste of the adventure.

    Fear not, brave developer! Your journey through the realms of videos and payments is about to
    reach new heights. May your callbacks resonate with victory and your code be as epic as the most
    legendary tales! 🌟🔮🚀
    serializer_class: PaymentSerializers = PaymentSerializers
    queryset = Payments.objects.all()
    pagination_class = CustomPagination
    payment = MoyasarAPIWrapper()
    lookup_field = "id"
    """

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
            return self.serializer_class.FetchPayment
        return self.serializer_class.GetPayment

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

    def get_plan_amount(self, plan):
        if plan == PaymentPlans.MONTHLY:
            return settings.MONTHLY_PLAN_PRICE
        else:
            return settings.ANNUAL_PLAN_PRICE

    @atomic
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - create: Prepare to wield the ultimate spell to conjure payments that seamlessly integrate with
        your video conquests! ✨🧙‍♂️
        Magic Scroll: POST
        Command: /payments/create

        Quest Tips:
        Channel your inner spellcaster to define the amount and payment plan. Our payment wizards
        will craft a seamless journey, complete with callbacks that align with your heroic quest.

        """
        user = request.user
        serializer = PaymentSerializers.CreatePayment(data=request.data)
        if serializer.is_valid(raise_exception=True):
            plan = serializer.validated_data.get("plan", None)
            amount = self.get_plan_amount(plan=plan)
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
            response = self.serializer_class.GetPayment(instance=instance)
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - list: Embark on a treasure hunt that reveals the riches of your VideoVerse accomplishments,
        guarded by loyal pagination guardians! 🗺️📜
        Explorer's Scroll: GET
        Command: /payments

        Quest Tips:
        Journey through the scrolls guided by our wise pagination guardians. Uncover your hard-earned
        treasures in bite-sized portions, making your exploration smooth and delightful.

        """
        page = self.paginate_queryset(self.get_queryset())
        data = self.serializer_class.GetPayment(instance=page, many=True).data
        return self.get_paginated_response(data)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - retrieve: Venture deeper into the realm as you unveil the secrets behind individual payments,
        adding a layer of mystique to your adventure! 🔍🤐
        Decoder Scroll: GET
        Command: /payments/{id}

        Quest Tips:
        Empower yourself to unravel the essence of a single payment. The response shall reveal the
        secrets you seek, letting you savor the thrill of discovery.

        """
        instance = self.get_object()
        response = self.serializer_class.FetchPayment(instance)
        return Response(response.data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - update: These sacred records are untouchable, holding ancient power.
        Approach with respect. Forbidden: 403
        """
        raise PermissionDenied(detail="You can't update a record")

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - partial_update: These sacred records are untouchable, holding ancient power.
        Approach with respect. Forbidden: 403
        """
        raise PermissionDenied(detail="You can't update a record")

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - destroy: The fabric of the realm shudders at the thought of deletion. Honor the balance and
        tread carefully. Forbidden: 403
        """
        raise PermissionDenied(detail="You can't delete a record")
