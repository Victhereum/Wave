from os.path import basename
from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from wave.apps.users.models import User
from wave.apps.video.models import Caption
from wave.apps.video.paginations import CustomPagination
from wave.apps.video.permissions import CanCreateCaption
from wave.apps.video.s3 import BunnyCaptionAPI
from wave.apps.video.serializers import CaptionSerializer
from wave.apps.video.translator import AzureSpeachService
from wave.utils.enums import FromLanguages, TaskLiterals, ToLanguages
from wave.utils.media import MediaHelper

fs = FileSystemStorage()


class CaptionViewSet(ModelViewSet):
    queryset = Caption.objects.all()
    serializer_class: CaptionSerializer = CaptionSerializer
    pagination_class = CustomPagination
    lookup_field = "id"
    permission_classes = [IsAuthenticated, CanCreateCaption]
    http_method_names = ["get", "post", "patch", "delete"]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self) -> QuerySet:
        self.queryset = Caption.objects.filter(user=self.request.user)
        return self.queryset

    @extend_schema(
        request=CaptionSerializer.CreateCaption,
        parameters=[CaptionSerializer.TranscriptionParams, CaptionSerializer.TranslationParams],
        responses={status.HTTP_200_OK: CaptionSerializer.GetCaption},
    )
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new caption
        """
        serializer = self.serializer_class.CreateCaption(data=request.data)
        if request.query_params.get("action", None) == TaskLiterals.TRANSLATE:
            serialized_params = self.serializer_class.TranslationParams(data=request.query_params)
        else:
            serialized_params = self.serializer_class.TranscriptionParams(data=request.query_params)
        if serializer.is_valid(raise_exception=True) and serialized_params.is_valid(raise_exception=True):
            resource = request.FILES.get("resource")
            from_lang = serialized_params.validated_data.pop("from_lang")
            to_lang = serialized_params.validated_data.pop("to_lang", "")
            action = serialized_params.validated_data.pop("action")
            # Save the uploaded file to a temporary location
            try:
                filename = fs.save(resource.name, resource)
                file_path = fs.path(filename)
                if "wave" not in resource.content_type:
                    file_path, name = MediaHelper.convert_to_wav(file_path)
                caption = AzureSpeachService(file_path, from_lang=from_lang, to_lang=to_lang)
                captioned_data = caption.perform(action=action)
                # Delete the temporary file after processing
                fs.delete(filename)
                fs.delete(name)

                video: Caption = Caption.objects.create(user=request.user, was_captioned=True, captions=captioned_data)
                response = self.serializer_class.GetCaption(video)
                return Response(response.data, status=status.HTTP_200_OK)
            except AttributeError:
                return Response({"resource": "The video seems to be corrupted"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CaptionSerializer.TranslateText,
        responses={status.HTTP_200_OK: CaptionSerializer.TextTranslationResponse},
    )
    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def text(self, request: Request, *args, **kwargs):
        """
        Create text to text translation
        """
        if translation_data := getattr(request, "translation_data"):
            serializer = self.serializer_class.TranslateText(data=translation_data)
            self.action = "text"
        else:
            serializer = self.serializer_class.TranslateText(data=request.data)
        serializer.is_valid(raise_exception=True)
        translation = AzureSpeachService(
            text=serializer.validated_data.get("text"), from_lang=FromLanguages.EN_US, to_lang=ToLanguages.ARABIC
        )
        translation_data = translation.perform(self.action)
        return Response(self.serializer_class.TextTranslationResponse(translation_data).data)

    @action(detail=False, methods=["GET"], permission_classes=[AllowAny])
    def rss(self, request: Request, *args, **kwargs):
        """
        This endpoint would fetch rss feeds from major rss feed providers, and translate it to Arabic
        """
        request.translation_data = AzureSpeachService.rss()
        return self.text(request=request)

    def build_url(self, *args, **kwargs) -> str:
        storage_zone = settings.STORAGE_ZONE_NAME
        return f"https://{storage_zone}.b-cdn.net/{self.user_identifier()}/{kwargs.get('file_name')}"

    def user_identifier(self, *args, **kwargs):
        user: User = self.request.user
        storage_zone = settings.STORAGE_ZONE_NAME
        collection = str(user.phone_no).removeprefix("+")
        if not user.collection_id:
            user.collection_id = f"https://sg.storage.bunnycdn.com/{storage_zone}/{collection}/"
            user.save()
        return collection

    @extend_schema(
        request=CaptionSerializer.UpdateCaption,
        responses={status.HTTP_202_ACCEPTED: CaptionSerializer.GetCaption},
        summary="Embed SRT to the video",
    )
    @transaction.atomic
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        This endpoint embeds the srt file to the video
        """
        instance = self.get_object()
        serializer = self.serializer_class.UpdateCaption(data=request.data)
        if serializer.is_valid(raise_exception=True):
            resource = serializer.validated_data.get("resource")
            srt = serializer.validated_data.pop("srt")
            try:
                resourcename = fs.save(resource.name, resource)
                srtname = fs.save(srt.name, srt)
                resource_path = fs.path(resourcename)
                srt_path = fs.path(srtname)

                output = MediaHelper.embed_srt_to_video(resource_path, srt_path)
                subtitle_output = Path(output)

                file_name = str(basename(subtitle_output)).replace(" ", "")
                response = BunnyCaptionAPI().upload_video(subtitle_output, self.user_identifier(), file_name)
                fs.delete(resourcename)
                fs.delete(srtname)
                fs.delete(output)

                serializer.validated_data.pop("resource")
                instance.resource = self.build_url(file_name=file_name)
                instance.name = file_name
                update = serializer.update(instance=instance, validated_data=serializer.validated_data)
                response = self.serializer_class.GetCaption(update)
                return Response(response.data, status=status.HTTP_202_ACCEPTED)
            except AttributeError as e:
                return Response(
                    {"resource": f"The video seems to be corrupted: {e}"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_200_OK: CaptionSerializer.ListCaption(many=True)})
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - List all caption projects
        """
        page = self.paginate_queryset(self.get_queryset())
        response = self.serializer_class.ListCaption(page, many=True)
        return self.get_paginated_response(response.data)

    @extend_schema(responses={status.HTTP_200_OK: CaptionSerializer.GetCaption})
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - Retrieve a caption project
        """
        response = self.serializer_class.GetCaption(self.get_object())
        return Response(response.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={status.HTTP_200_OK: CaptionSerializer.FromLanguageResponseSerializer(many=True)},
        summary="List of languages to be used in from_lang parameter",
    )
    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def from_languages(self, request, *args, **kwargs):
        """List of languages to be used in from_lang parameter"""
        choices = ({"value": choice[0], "label": choice[1]} for choice in FromLanguages.choices)
        return Response(choices)

    @extend_schema(
        responses={status.HTTP_200_OK: CaptionSerializer.ToLanguageResponseSerializer(many=True)},
        summary="List of languages to be used in to_lang parameter",
    )
    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def to_languages(self, request, *args, **kwargs):
        """List of languages to be used in to_lang parameter"""

        choices = ({"value": choice[0], "label": choice[1]} for choice in ToLanguages.choices)
        return Response(choices)

    @extend_schema(
        responses={status.HTTP_200_OK: CaptionSerializer.ToLanguageResponseSerializer(many=True)},
        summary="List of languages to be used in languages parameter",
    )
    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def languages(self, request, *args, **kwargs):
        choices = {
            "from_languages": ({"value": choice[0], "label": choice[1]} for choice in FromLanguages.choices),
            "to_languages": ({"value": choice[0], "label": choice[1]} for choice in ToLanguages.choices),
        }
        return Response(choices)

    def destroy(self, request, *args, **kwargs):
        instance: Caption = self.get_object()
        # Remove the file from bunny
        BunnyCaptionAPI().delete_video(self.user_identifier(), instance.name)
        return super().destroy(request, **args, **kwargs)
