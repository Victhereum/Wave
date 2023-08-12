from rest_framework import serializers

from wave.apps.video.models import Video
from wave.utils.choices import LanguageChoices, TaskLiterals


class VideoSerializer:
    class Create(serializers.ModelSerializer):
        task = serializers.ChoiceField(choices=TaskLiterals.choices)
        language = serializers.ChoiceField(choices=LanguageChoices.choices, default=LanguageChoices.OTHERS)

        class Meta:
            model = Video
            fields = (
                "language",
                "task",
            )

    class Get(serializers.ModelSerializer):
        class Meta:
            model = Video
            exclude = ("visible", "user")

    class List(serializers.ModelSerializer):
        class Meta:
            model = Video
            exclude = ("visible", "user", "captions")

    class Fetch(serializers.ModelSerializer):
        class Meta:
            model = Video
            exclude = ("visible",)

    class Update(serializers.ModelSerializer):
        media_path = serializers.CharField(required=True)
        captions = serializers.JSONField(required=False)

        class Meta:
            model = Video
            fields = ("media_path", "captions")
