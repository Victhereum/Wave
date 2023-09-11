from rest_framework import serializers

from wave.apps.video.models import Video
from wave.utils.enums import LanguageChoices, TaskLiterals


class VideoSerializer:
    class CreateVideo(serializers.Serializer):
        media = serializers.FileField(required=True)

        class Meta:
            #     # model = Video
            fields = ("media",)

    class CreateVideoParams(serializers.Serializer):
        from_lang = serializers.ChoiceField(choices=LanguageChoices.choices, default=LanguageChoices.OTHERS)
        to_lang = serializers.ChoiceField(choices=LanguageChoices.choices, default=LanguageChoices.OTHERS)
        action = serializers.ChoiceField(choices=TaskLiterals.choices, default=TaskLiterals.TRANSLATE)

        class Meta:
            #     # model = Video
            fields = [
                "from_lang",
                "to_lang",
                "action",
            ]

    class GetVideo(serializers.ModelSerializer):
        class Meta:
            model = Video
            fields = ("media_path", "was_captioned", "captions")

    class ListVideo(serializers.ModelSerializer):
        class Meta:
            model = Video
            exclude = ("visible", "user", "captions")

    class FetchVideo(serializers.ModelSerializer):
        class Meta:
            model = Video
            exclude = ("visible",)

    class UpdateVideo(serializers.ModelSerializer):
        media_path = serializers.CharField(required=True)
        captions = serializers.JSONField(required=False)

        class Meta:
            model = Video
            fields = ("media_path", "captions")

    class ResultSerializer(serializers.Serializer):
        result = serializers.JSONField()
