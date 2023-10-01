from rest_framework import serializers

from wave.apps.video.models import Video
from wave.utils.enums import FromLanguages, TaskLiterals, ToLanguages


class VideoSerializer:
    class CreateVideo(serializers.Serializer):
        media = serializers.FileField(required=True)

        class Meta:
            #     # model = Video
            fields = ("media",)

    class TranslateVideoParams(serializers.Serializer):
        from_lang = serializers.ChoiceField(choices=FromLanguages.choices, default=FromLanguages.OTHERS)
        to_lang = serializers.ChoiceField(choices=ToLanguages.choices, default=ToLanguages.OTHERS)
        action = serializers.ChoiceField(choices=TaskLiterals.choices, default=TaskLiterals.TRANSLATE)

        class Meta:
            #     # model = Video
            fields = [
                "from_lang",
                "to_lang",
                "action",
            ]

    class TranscribleVideoParams(serializers.Serializer):
        from_lang = serializers.ChoiceField(choices=FromLanguages.choices, default=FromLanguages.OTHERS)
        action = serializers.ChoiceField(choices=TaskLiterals.choices, default=TaskLiterals.TRANSCRIBE)

        class Meta:
            #     # model = Video
            fields = [
                "from_lang",
                "action",
            ]

    class FromLanguageSerializer(serializers.Serializer):
        languages = serializers.ChoiceField(choices=FromLanguages.choices, default=FromLanguages.OTHERS)

        class Meta:
            #     # model = Video
            fields = [
                "languages",
            ]

    class ToLanguageSerializer(serializers.Serializer):
        languages = serializers.ChoiceField(choices=ToLanguages.choices, default=FromLanguages.OTHERS)

        class Meta:
            #     # model = Video
            fields = [
                "languages",
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
