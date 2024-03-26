from rest_framework import serializers

from wave.apps.video.models import Caption
from wave.utils.enums import FromLanguages, TaskLiterals, ToLanguages
from wave.utils.validators import FileValidatorHelper


class CaptionSerializer:
    class CreateCaption(serializers.Serializer):
        resource = serializers.FileField(required=True)

        class Meta:
            #     # model = Caption
            fields = ("resource",)

    class TranslateText(serializers.Serializer):
        text = serializers.CharField(required=True)

        class Meta:
            #     # model = Caption
            fields = ("text",)

    class TextTranslationResponse(serializers.Serializer):
        translations = serializers.ListField(child=serializers.JSONField(read_only=True))

    class TranslationParams(serializers.Serializer):
        from_lang = serializers.ChoiceField(choices=FromLanguages.choices, default=FromLanguages.OTHERS)
        to_lang = serializers.ChoiceField(choices=ToLanguages.choices, default=ToLanguages.OTHERS)
        action = serializers.ChoiceField(choices=TaskLiterals.choices, default=TaskLiterals.TRANSLATE)

        class Meta:
            #     # model = Caption
            fields = [
                "from_lang",
                "to_lang",
                "action",
            ]

    class TranscriptionParams(serializers.Serializer):
        from_lang = serializers.ChoiceField(choices=FromLanguages.choices, default=FromLanguages.OTHERS)
        action = serializers.ChoiceField(choices=TaskLiterals.choices, default=TaskLiterals.TRANSCRIBE)

        class Meta:
            #     # model = Caption
            fields = [
                "from_lang",
                "action",
            ]

    class FromLanguageSerializer(serializers.Serializer):
        languages = serializers.ChoiceField(choices=FromLanguages.choices, default=FromLanguages.OTHERS)

        class Meta:
            #     # model = Caption
            fields = [
                "languages",
            ]

    class FromLanguageResponseSerializer(serializers.Serializer):
        value = serializers.ChoiceField(choices=[x[0] for x in FromLanguages.choices])
        label = serializers.ChoiceField(choices=[x[1] for x in FromLanguages.choices])

    class ToLanguageSerializer(serializers.Serializer):
        languages = serializers.ChoiceField(choices=ToLanguages.choices, default=FromLanguages.OTHERS)

        class Meta:
            #     # model = Caption
            fields = [
                "languages",
            ]

    class ToLanguageResponseSerializer(serializers.Serializer):
        value = serializers.ChoiceField(choices=[x[0] for x in ToLanguages.choices])
        label = serializers.ChoiceField(choices=[x[1] for x in ToLanguages.choices])

    class GetCaption(serializers.ModelSerializer):
        class Meta:
            model = Caption
            fields = ("id", "resource_path", "was_captioned", "resource", "captions")

    class ListCaption(serializers.ModelSerializer):
        class Meta:
            model = Caption
            exclude = ("visible", "user", "captions")

    class FetchCaption(serializers.ModelSerializer):
        class Meta:
            model = Caption
            exclude = ("visible",)

    class UpdateCaption(serializers.ModelSerializer):
        resource_path = serializers.CharField(required=True)
        captions = serializers.JSONField(required=False)
        resource = serializers.FileField(
            validators=[FileValidatorHelper.validate_video_extension, FileValidatorHelper.validate_video_size]
        )
        srt = serializers.FileField(
            validators=[FileValidatorHelper.validate_subtitle_extension, FileValidatorHelper.validate_subtitle_size],
            write_only=True,
        )

        class Meta:
            model = Caption
            fields = ("resource_path", "captions", "srt", "resource")

    class ResultSerializer(serializers.Serializer):
        result = serializers.JSONField()


class LanguageSerializer(serializers.Serializer):
    from_languages = CaptionSerializer.FromLanguageResponseSerializer(many=True)
    to_languages = CaptionSerializer.ToLanguageResponseSerializer(many=True)
