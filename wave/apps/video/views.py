from typing import Any

from django.core.files.storage import FileSystemStorage
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from wave.apps.video.models import Video
from wave.apps.video.paginations import CustomPagination
from wave.apps.video.serializers import VideoSerializer
from wave.utils.translator import OpenAIWhisper


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class: VideoSerializer = VideoSerializer
    pagination_class = CustomPagination
    lookup_field = "id"

    def get_queryset(self) -> QuerySet:
        self.queryset = Video.objects.filter(user=self.request.user)
        return self.queryset

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class.Create(data=request.data)
        if serializer.is_valid(raise_exception=True):
            media = request.FILES.get("media")
            task = serializer.validated_data.pop("task")
            language = serializer.validated_data.pop("language")
            # Save the uploaded file to a temporary location
            fs = FileSystemStorage()
            filename = fs.save(media.name, media)
            file_path = fs.path(filename)

            caption = OpenAIWhisper(file_path, task=task, lang=language)
            captioned_data = caption.transcribe_media()
            # Delete the temporary file after processing
            fs.delete(filename)
            media = Video.objects.create(user=request.user, captions=captioned_data, was_captioned=True)
            response = self.serializer_class.Get(media)
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.serializer_class.Update(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = self.get_object()
            update = serializer.update(instance=instance, validated_data=serializer.validated_data)
            response = self.serializer_class.Get(update)
            return Response(response.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        page = self.paginate_queryset(self.get_queryset())
        response = self.serializer_class.List(page, many=True)
        return self.get_paginated_response(response.data)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = self.serializer_class.Get(self.get_object())
        return Response(response.data, status=status.HTTP_200_OK)
