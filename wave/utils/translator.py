from typing import Literal

import openai
from django.conf import settings

from wave.utils.choices import LanguageChoices, TaskLiterals


class OpenAIWhisper:
    # Initialize your OpenAI API key
    openai.api_key = settings.OPEN_AI_KEY

    def __init__(
        self,
        media_path,
        task: Literal[TaskLiterals.TRANSLATE, TaskLiterals.TRANSCRIBE] = TaskLiterals.TRANSCRIBE,
        lang: str = "en",
    ) -> None:
        self._media_path = media_path
        self._lang = lang
        self._task = task

        self._params = {
            "response_format": "verbose_json",
            "temperature": 0.2,
        }
        # Prepare the params
        if self._lang != LanguageChoices.OTHERS:
            self._params["lang"] = self._lang

    @staticmethod
    def _decode_unicode_text(json_dict):
        def _decode_unicode(text):
            return b"".join(text).decode("utf-8")

        def _traverse_and_decode(obj):
            if isinstance(obj, dict):
                new_obj = {}
                for key, value in obj.items():
                    if isinstance(value, list) and key == "text":
                        byte_tokens = []
                        for t in value:
                            if t.startswith("\\u06"):
                                char_int = int(t[4:], base=16)
                                byte_tokens.append(bytes([char_int]))
                            else:
                                byte_tokens.append(t.encode())
                        new_obj[key] = [_decode_unicode(byte_tokens)]
                    elif key == "segments":
                        new_segments = []
                        for segment in value:
                            text = segment.get("text")
                            if text.startswith("\\u06"):
                                char_int = int(text[4:], base=16)
                                byte_tokens = [bytes([char_int])]
                            else:
                                byte_tokens = [text.encode()]
                            new_segment = segment.copy()
                            new_segment["text"] = _decode_unicode(byte_tokens)
                            new_segments.append(new_segment)
                        new_obj[key] = new_segments
                    elif isinstance(value, (dict, list)):
                        new_obj[key] = _traverse_and_decode(value)
                    else:
                        new_obj[key] = value
                return new_obj
            elif isinstance(obj, list):
                new_list = []
                for item in obj:
                    new_list.append(_traverse_and_decode(item))
                return new_list

        decoded_dict = json_dict.copy()
        _traverse_and_decode(decoded_dict)
        return decoded_dict

    def transcribe_media(self) -> dict:
        media_file_path = self._media_path
        # Read the media file
        with open(media_file_path, "rb") as media_file:
            if self._task == "transcribe":
                transcription_result = openai.Audio.transcribe(
                    **self._params,
                    model="whisper-1",
                    file=media_file,
                )
            else:
                transcription_result = openai.Audio.translate(
                    **self._params,
                    model="whisper-1",
                    file=media_file,
                )
            # decoded_data = self._decode_unicode_text(json.loads(str(transcription_result)))
            decoded_data = transcription_result

        return decoded_data
