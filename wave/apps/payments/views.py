import re
from typing import Any

from django.conf import settings
from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from wave.apps.payments.models import Payments
from wave.apps.payments.paginations import CustomPagination
from wave.apps.payments.serializers import PaymentSerializers
from wave.utils.custom_exceptions import CustomError
from wave.utils.enums import CurrencyChoices, PaymentPlans
from wave.utils.payments import MoyasarAPIWrapper


class PaymentViewSet(ModelViewSet):
    """
    PaymentViewSet: Level Up Your Video Quest with Payment Magic

    Greetings, fellow adventurers of the WaveVerse! 🎮💰 Welcome to the realm of Payments,
    where your heroic endeavors with videos are about to get a powerful upgrade. Gear up for an
    exhilarating journey as we blend the forces of videos and payments into one epic tale.

    The Chronicles Begin:
    Get ready to step into a world where videos meet payments in perfect harmony. Payments
    emerges as your trusty guide, enhancing your WaveVerse experience like never before!

    Payment Sorcery:
    - create: Prepare to wield the ultimate spell to conjure payments that seamlessly integrate with
      your video conquests! ✨🧙‍♂️
      Magic Scroll: POST
      Command: /payments/

      Quest Tips:
      Channel your inner spellcaster to defining your payment plan. Our payment wizards
      will craft a seamless journey, complete with callbacks that align with your heroic quest.

    - list: Embark on a treasure hunt that reveals the riches of your WaveVerse accomplishments,
      guarded by loyal pagination guardians! 🗺️📜
      Explorer's Scroll: GET
      Command: /payments/

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
    http_method_names = ["get", "post"]

    def month_number_to_text(self, month_number: int):
        """
        Convert a month number to its corresponding month name.

        Parameters:
            month_number (int): The number of the month to be converted.

        Returns:
            str: The name of the month if the number is valid, otherwise "Invalid Month".
        """
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
        """
        Returns the callback URL for the current request.

        :param self: The instance of the class.
        :return: The callback URL as a string.
        """
        return f"{self.request.build_absolute_uri()}"

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

    def dollars_to_cents(self, dollars: float) -> int:
        cents = int(dollars * 100)
        return cents

    def get_plan_amount(self, plan: str) -> int:
        """
        Calculates and returns the amount for a given payment plan.

        Parameters:
        - plan (PaymentPlans): The type of payment plan to calculate the amount for.

        Returns:
        - float: The amount for the given payment plan.

        Raises:
        - ValueError: If an invalid payment plan is provided.
        """
        if plan == PaymentPlans.BASIC:
            return self.dollars_to_cents(settings.BASIC_PLAN_PRICE)
        if plan == PaymentPlans.PRO:
            return self.dollars_to_cents(settings.PRO_PLAN_PRICE)
        if plan == PaymentPlans.ANNUAL:
            return self.dollars_to_cents(settings.PREMIUM_PLAN_PRICE)
        raise ValueError

    def get_card_type(self, card_number):
        # Remove any spaces or non-digit characters from the card number
        card_number = "".join(filter(str.isdigit, card_number))
        mada_pattern = (
            r"^(4(0(0861|1757|3024|6136|6996|7(197|395)|9201)|"
            r"1(2565|0621|0685|7633|9593)|2(0132|1141|281(7|8|9)|689700|8(331|67(1|2|3)))|"
            r"3(1361|2328|4107|9954)|4(0(533|647|795)|5564|6(393|404|672))|"
            r"5(5(036|708)|7865|7997|8456)|6(2220|854(0|1|2|3))|7(4491)|"
            r"8(301(0|1|2)|4783|609(4|5|6)|931(7|8|9))|93428)|"
            r"5(0(4300|6968|8160)|13213|2(0058|1076|4(130|514)|9(415|741))|"
            r"3(0(060|906)|1(095|196)|2013|5(825|989)|6023|7767|9931)|"
            r"4(3(085|357)|9760)|5(4180|7606|8563|8848)|"
            r"8(5265|8(8(4(5|6|7|8|9)|5(0|1))|98(2|3))|9(005|206)))|"
            r"6(0(4906|5141)|36120)|9682(0(1|2|3|4|5|6|7|8|9)|1(0|1)))"
        )
        # Define regular expressions for card types and their patterns
        card_patterns = {
            "mada": mada_pattern,
            "visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
            "mastercard": r"^(5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)\d{12}$",
            "american_express": r"^3[47][0-9]{13}$",
        }

        # Check the card number against the patterns
        for card_type, pattern in card_patterns.items():
            if re.match(pattern, card_number):
                print(card_type)
                print(card_type)
                print(card_type)
                print(card_type)
                return card_type
        raise ValidationError("Card company is invalid")

    def get_icon(self, company):
        icons = {
            "visa": "https://iconape.com/wp-content/files/de/370236/svg/370236.svg",
            "mada": "https://iconape.com/wp-content/files/yo/366974/svg/366974.svg",
            "mastercard": "https://iconape.com/wp-content/files/gt/371249/svg/371249.svg",
            "american_express": "https://iconape.com/wp-content/files/im/184198/svg/184198.svg",
        }

        return icons.get(company)

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
            # month_text = self.month_number_to_text(month_number=int(datetime.now().date().month))
            # plan_description = month_text if plan == PaymentPlans.MONTHLY else datetime.now().date().year
            description = f"Wave payment from {user.name} for {plan} Plan"
            source: dict = serializer.validated_data.pop("source", {})
            source.update(
                {
                    "company": self.get_card_type(source.get("number", "")),
                }
            )
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

    def plans(self, request: Request, *args, **kwargs):
        """
        Returns all payment plans, their prices and descriptions
        """
        # TODO: List all payment plans, description, priviledges and prices

    @action(detail=False, methods=["get"])
    def currencies(self, request, *args, **kwargs):
        choices = ({"value": choice[0], "label": choice[1]} for choice in CurrencyChoices.choices)
        return Response(choices)

    @action(detail=False, methods=["get"])
    def card_type(self, request, *args, **kwargs):
        serializer = self.serializer_class.CardType(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            company = self.get_card_type(serializer.validated_data.get("number", ""))
            choices = {
                "value": company,
                "label": company.title().replace(
                    "_",
                    " ",
                ),
                "icon": self.get_icon(company),
            }
            return Response(choices)
        return Response(serializer.errors)
