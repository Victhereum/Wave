from typing import Any

from django.core.files.storage import FileSystemStorage
from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from wave.apps.video.models import Video
from wave.apps.video.paginations import CustomPagination
from wave.apps.video.serializers import VideoSerializer
from wave.utils.translator import OpenAIWhisper


class VideoViewSet(ModelViewSet):
    """
    VideoViewSet: Taming Videos with Swagger Swagger

    Whether you're a frontend developer, backend wizard, or a unicorn enthusiast, welcome to the realm
    of VideoViewSet! 🎥✨ Let's dive into the epic saga of handling videos in a way that even Gandalf
    would be proud of.

    Description:
    VideoViewSet is your trusty companion for managing videos like a pro. It's not just a view, it's
    a view with style and swagger, ready to slay dragons and transcribe videos. 🐉

    Methods:
    - create:
        Use this mystical spell to create a new video with captions that even Shakespeare would envy.
        HTTP Method: POST
        Path: /api/v1/videos/

        Wizard's Tip:
        Supply your media file and the type of task you want the video to perform. The sorcery behind
        the scenes will transcribe your video and craft you a magic response.

    - partial_update:
        Partial updates for when you need to give your video a makeover without breaking the spell.
        HTTP Method: PATCH
        Path: /api/v1/videos/{id}/

        Wizard's Tip:
        Tweak the media path and captions of your video. Our wizards will ensure your updates are
        gracefully accepted or met with a 400 BAD REQUEST spell.

    - list:
        Retrieve a list of your enchanted videos, safely guarded by your own user shield.
        HTTP Method: GET
        Path: /api/v1/videos/

        Wizard's Tip:
        Paginate your way through your videos. Gather them in small, friendly clusters to avoid
        overwhelming even the bravest of browsers.

    - retrieve:
        Summon the details of a single video by invoking its unique identifier.
        HTTP Method: GET
        Path: /api/v1/videos/{id}

        Wizard's Tip:
        Retrieve the mystical knowledge of a specific video. The video's secrets shall be revealed in
        a splendid 200 OK response.

    Sidekicks:
    Meet your trusty sidekicks, the powerful serializers, ready to translate your requests and
    responses between different dimensions.
    - VideoSerializer.Create: Use this to channel your creativity when creating a video. Specify the
      task and language, and witness the magic unfold.
    - VideoSerializer.Get: The master of ceremonies when revealing video secrets. This serializer
      unveils the beauty of a video.
    - VideoSerializer.List: For those moments when you need to showcase your collection of videos.
      Tame the list with elegance.
    - VideoSerializer.Update: When your video craves updates, this is your go-to spell. Adjust the
      media path and captions with grace.

    Remember, brave developer, you are the commander of these views. May your APIs be as smooth as
    butter and your code as elegant as a dragon's dance. 🐲👩‍💻🚀
    """

    queryset = Video.objects.all()
    serializer_class: VideoSerializer = VideoSerializer
    pagination_class = CustomPagination
    lookup_field = "id"

    def get_serializer(self, *args, **kwargs) -> BaseSerializer:
        if self.action == "create":
            return self.serializer_class.CreateVideo(*args, **kwargs)
        elif self.action == "partial_update":
            return self.serializer_class.UpdateVideo(*args, **kwargs)
        elif self.action in ["list", "retrieve"]:
            return self.serializer_class.GetVideo(*args, **kwargs)
        return self.serializer_class.GetVideo(*args, **kwargs)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "create":
            return self.serializer_class.CreateVideo
        elif self.action == "partial_update":
            return self.serializer_class.UpdateVideo
        elif self.action in ["list", "retrieve"]:
            return self.serializer_class.GetVideo
        return self.serializer_class.GetVideo

    def get_queryset(self) -> QuerySet:
        self.queryset = Video.objects.filter(user=self.request.user)
        return self.queryset

    @extend_schema(request=VideoSerializer.CreateVideo, responses={status.HTTP_200_OK: VideoSerializer.GetVideo})
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - create:
        Use this mystical spell to create a new video with captions that even Shakespeare would envy.
        HTTP Method: POST
        Path: /api/v1/videos/

        Wizard's Tip:
        Supply your media file and the type of task you want the video to perform. The sorcery behind
        the scenes will transcribe your video and craft you a magic response.
        """
        serializer = self.serializer_class.CreateVideo(data=request.data)
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
            response = self.serializer_class.GetVideo(media)
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - partial_update:
        Partial updates for when you need to give your video a makeover without breaking the spell.
        HTTP Method: PATCH
        Path: /api/v1/videos/{id}/

        Wizard's Tip:
        Tweak the media path and captions of your video. Our wizards will ensure your updates are
        gracefully accepted or met with a 400 BAD REQUEST spell.
        """
        serializer = self.serializer_class.UpdateVideo(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = self.get_object()
            update = serializer.update(instance=instance, validated_data=serializer.validated_data)
            response = self.serializer_class.GetVideo(update)
            return Response(response.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - list:
        Retrieve a list of your enchanted videos, safely guarded by your own user shield.
        HTTP Method: GET
        Path: /api/v1/videos/

        Wizard's Tip:
        Paginate your way through your videos. Gather them in small, friendly clusters to avoid
        overwhelming even the bravest of browsers.
        """
        page = self.paginate_queryset(self.get_queryset())
        response = self.serializer_class.ListVideo(page, many=True)
        return self.get_paginated_response(response.data)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        - retrieve:
        Summon the details of a single video by invoking its unique identifier.
        HTTP Method: GET
        Path: /api/v1/videos/{id}

        Wizard's Tip:
        Retrieve the mystical knowledge of a specific video. The video's secrets shall be revealed in
        a splendid 200 OK response.
        """
        response = self.serializer_class.GetVideo(self.get_object())
        return Response(response.data, status=status.HTTP_200_OK)
