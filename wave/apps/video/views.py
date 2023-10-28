from pathlib import Path
from typing import Any

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from wave.apps.video.models import Video
from wave.apps.video.paginations import CustomPagination
from wave.apps.video.permissions import CanCreateVideo
from wave.apps.video.s3 import BunnyVideoAPI
from wave.apps.video.serializers import VideoSerializer
from wave.apps.video.translator import AzureSpeachService
from wave.utils.enums import FromLanguages, TaskLiterals, ToLanguages
from wave.utils.media import MediaHelper

fs = FileSystemStorage()


class VideoViewSet(ModelViewSet):
    """
    VideoViewSet: Taming Videos with AI

    Whether you're a frontend developer, backend wizard, or a unicorn enthusiast, welcome to the realm
    of Wave video endpoints! 🎥✨ Let's dive into the epic saga of handling videos in a way that even Gandalf
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
    permission_classes = [IsAuthenticated, CanCreateVideo]
    http_method_names = ["get", "post", "patch"]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer(self, *args, **kwargs) -> BaseSerializer:
        if self.action == "create":
            return self.serializer_class.CreateVideo(*args, **kwargs)
        elif self.action == "partial_update":
            return self.serializer_class.UpdateVideo(*args, **kwargs)
        elif self.action in ["list", "retrieve"]:
            return self.serializer_class.GetVideo(*args, **kwargs)
        elif self.action in "to_languages":
            return self.serializer_class.ToLanguageSerializer(*args, **kwargs)
        elif self.action in "from_languages":
            return self.serializer_class.FromLanguageSerializer(*args, **kwargs)
        return self.serializer_class.GetVideo(*args, **kwargs)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.action == "create":
            return self.serializer_class.CreateVideo
        elif self.action == "partial_update":
            return self.serializer_class.UpdateVideo
        elif self.action in ["list", "retrieve"]:
            return self.serializer_class.GetVideo
        elif self.action in "to_languages":
            return self.serializer_class.ToLanguageSerializer
        elif self.action in "from_languages":
            return self.serializer_class.FromLanguageSerializer
        return self.serializer_class.GetVideo

    def get_queryset(self) -> QuerySet:
        self.queryset = Video.objects.filter(user=self.request.user)
        return self.queryset

    @extend_schema(
        request=VideoSerializer.CreateVideo,
        parameters=[VideoSerializer.TranscribleVideoParams, VideoSerializer.TranslateVideoParams],
        responses={status.HTTP_200_OK: VideoSerializer.GetVideo},
    )
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
        if request.query_params.get("action", None) == TaskLiterals.TRANSLATE:
            serialized_params = self.serializer_class.TranslateVideoParams(data=request.query_params)
        else:
            serialized_params = self.serializer_class.TranscribleVideoParams(data=request.query_params)
        if serializer.is_valid(raise_exception=True) and serialized_params.is_valid(raise_exception=True):
            media = request.FILES.get("media")
            from_lang = serialized_params.validated_data.pop("from_lang")
            to_lang = serialized_params.validated_data.pop("to_lang", "")
            action = serialized_params.validated_data.pop("action")
            # Save the uploaded file to a temporary location
            try:
                filename = fs.save(media.name, media)
                file_path = fs.path(filename)
                if "wave" not in media.content_type:
                    file_path, name = MediaHelper.convert_to_wav(file_path)
                caption = AzureSpeachService(file_path, from_lang=from_lang, to_lang=to_lang)
                captioned_data = caption.perform(action=action)
                # Delete the temporary file after processing
                fs.delete(filename)
                fs.delete(name)

                video: Video = Video.objects.create(user=request.user, was_captioned=True, captions=captioned_data)
                response = self.serializer_class.GetVideo(video)
                return Response(response.data, status=status.HTTP_200_OK)
            except AttributeError:
                return Response({"media": "The video seems to be corrupted"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def build_url(video_id: str) -> str:
        library_id = settings.CDN_LIBRARY
        return f"https://video.bunnycdn.com/library/{library_id}/videos/{video_id}"

    def get_or_create_user_collection(self):
        user = self.request.user
        if guid := user.collection_id:
            print("THE GUID", guid)
            return guid
        response = BunnyVideoAPI().create_collection(user.phone_no)
        print("CREATE COLLECTION RESPONSE", response)
        guid = response.get("guid")
        user.collection_id = guid
        user.save()
        return guid

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        serializer = self.serializer_class.UpdateVideo(data=request.data)
        if serializer.is_valid(raise_exception=True):
            media = serializer.validated_data.get("media")
            srt = serializer.validated_data.get("srt")
            try:
                medianame = fs.save(media.name, media)
                srtname = fs.save(srt.name, srt)
                media_path = fs.path(medianame)
                srt_path = fs.path(srtname)

                print("EMBEDING SRT TO VIDEO")
                output = MediaHelper.embed_srt_to_video(media_path, srt_path)
                subtitle_output = Path(output)

                collection_id = self.get_or_create_user_collection()
                print("SENDING VIDEO TO BUNNY")
                response = BunnyVideoAPI().upload_video(media.name, subtitle_output, collection_id)
                print("CREATE VIDEO RESPONSE", response)
                fs.delete(medianame)
                fs.delete(srtname)
                fs.delete(output)

                print("WRAPPING UP")
                serializer.validated_data.pop("media")
                instance.media = self.build_url(response.get("guid"))
                update = serializer.update(instance=instance, validated_data=serializer.validated_data)
                response = self.serializer_class.GetVideo(update)
                return Response(response.data, status=status.HTTP_202_ACCEPTED)
            except AttributeError as e:
                return Response({"media": f"The video seems to be corrupted: {e}"}, status=status.HTTP_400_BAD_REQUEST)
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

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def from_languages(self, request, *args, **kwargs):
        """List of languages to be used in from_lang parameter"""
        choices = ({"value": choice[0], "label": choice[1]} for choice in FromLanguages.choices)
        return Response(choices)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def to_languages(self, request, *args, **kwargs):
        """List of languages to be used in to_lang parameter"""

        choices = ({"value": choice[0], "label": choice[1]} for choice in ToLanguages.choices)
        return Response(choices)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def languages(self, request, *args, **kwargs):
        choices = {
            "from_languages": ({"value": choice[0], "label": choice[1]} for choice in FromLanguages.choices),
            "to_languages": ({"value": choice[0], "label": choice[1]} for choice in ToLanguages.choices),
        }
        return Response(choices)
