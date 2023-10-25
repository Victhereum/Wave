import json
import time
from datetime import timedelta

import azure.cognitiveservices.speech as speechsdk

# import openai
from django.conf import settings

from wave.apps.video.serializers import VideoSerializer

# from wave.utils.enums import LanguageChoices, TaskLiterals

ENDPOINT = settings.AZURE_SERVICE_ENDPOINT
SERVICE_KEY = settings.AZURE_SERVICE_KEY
SERVICE_REGION = settings.AZURE_SERVICE_REGION


# class OpenAIWhisper:
#     # Initialize your OpenAI API key
#     openai.api_key = settings.OPEN_AI_KEY

#     def __init__(
#         self,
#         media_path,
#         task: Literal[TaskLiterals.TRANSLATE, TaskLiterals.TRANSCRIBE] = TaskLiterals.TRANSCRIBE,
#         lang: str = "en",
#     ) -> None:
#         self._media_path = media_path
#         self._lang = lang
#         self._task = task

#         self._params = {
#             "response_format": "verbose_json",
#             "temperature": 0.2,
#         }
#         # Prepare the params
#         if self._lang != LanguageChoices.OTHERS:
#             self._params["lang"] = self._lang

#     @staticmethod
#     def _decode_unicode_text(json_dict):
#         def _decode_unicode(text):
#             return b"".join(text).decode("utf-8")

#         def _traverse_and_decode(obj):
#             if isinstance(obj, dict):
#                 new_obj = {}
#                 for key, value in obj.items():
#                     if isinstance(value, list) and key == "text":
#                         byte_tokens = []
#                         for t in value:
#                             if t.startswith("\\u06"):
#                                 char_int = int(t[4:], base=16)
#                                 byte_tokens.append(bytes([char_int]))
#                             else:
#                                 byte_tokens.append(t.encode())
#                         new_obj[key] = [_decode_unicode(byte_tokens)]
#                     elif key == "segments":
#                         new_segments = []
#                         for segment in value:
#                             text = segment.get("text")
#                             if text.startswith("\\u06"):
#                                 char_int = int(text[4:], base=16)
#                                 byte_tokens = [bytes([char_int])]
#                             else:
#                                 byte_tokens = [text.encode()]
#                             new_segment = segment.copy()
#                             new_segment["text"] = _decode_unicode(byte_tokens)
#                             new_segments.append(new_segment)
#                         new_obj[key] = new_segments
#                     elif isinstance(value, (dict, list)):
#                         new_obj[key] = _traverse_and_decode(value)
#                     else:
#                         new_obj[key] = value
#                 return new_obj
#             elif isinstance(obj, list):
#                 new_list = []
#                 for item in obj:
#                     new_list.append(_traverse_and_decode(item))
#                 return new_list

#         decoded_dict = json_dict.copy()
#         _traverse_and_decode(decoded_dict)
#         return decoded_dict

#     def transcribe_media(self) -> dict:
#         media_file_path = self._media_path
#         # Read the media file
#         with open(media_file_path, "rb") as media_file:
#             if self._task == "transcribe":
#                 transcription_result = openai.Audio.transcribe(
#                     **self._params,
#                     model="whisper-1",
#                     file=media_file,
#                 )
#             else:
#                 transcription_result = openai.Audio.translate(
#                     **self._params,
#                     model="whisper-1",
#                     file=media_file,
#                 )
#             # decoded_data = self._decode_unicode_text(json.loads(str(transcription_result)))
#             decoded_data = transcription_result

#         return decoded_data


def map_translations_to_audio_words(translations: str, words_with_timestamps: list[dict]) -> list[dict]:
    # Split the translations string by spaces and remove any occurrences of "،"
    translations = translations.replace("،", "").split(" ")

    # Create a list comprehension to generate the new words with timestamps
    new_words_with_timestamps = [
        {
            "Word": word,
            "Offset": f'{timedelta(milliseconds=(current_word["Offset"]/10000))}',
            "Duration": f'{timedelta(milliseconds=(current_word["Duration"]/10000))}',
        }
        for word, current_word in zip(translations, words_with_timestamps)
    ]

    # Return the list of new words with timestamps
    return new_words_with_timestamps


def to_representation(words_with_timestamps: list[dict]) -> list[dict]:
    # Split the translations string by spaces and remove any occurrences of "،"

    # Create a list comprehension to generate the new words with timestamps
    new_words_with_timestamps = [
        {
            "Word": current_word["Word"],
            "Offset": f'{timedelta(milliseconds=(current_word["Offset"]/10000))}',
            "Duration": f'{timedelta(milliseconds=(current_word["Duration"]/10000))}',
        }
        for current_word in words_with_timestamps
    ]

    # Return the list of new words with timestamps
    return new_words_with_timestamps


class AzureSpeachService:
    def __init__(
        self,
        media_path,
        from_lang: str = "en",
        to_lang: str = "en",
    ) -> None:
        self._media_path = media_path
        self._from_lang = from_lang
        self._to_lang = to_lang

    result = []

    def perform(self, action: str) -> list[dict]:
        """
        Perform the specified action and return the result.

        Args:
            action (str, optional): The action to perform. Defaults to "transcribe".

        Returns:
            List[dict]: The result of the action.
        """
        assert action
        actions = {"translate": self.translate, "transcribe": self.transcribe}
        return actions.get(action)()

    def translate(self) -> list[dict]:
        self.result = []
        print("TRANSLATING")
        # Configure the speech translation settings
        speech_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=SERVICE_KEY, endpoint=ENDPOINT, target_languages=[self._to_lang]
        )
        # Enable word-level timestamps
        speech_config.request_word_level_timestamps()
        # Set the speech recognition language to the source language
        speech_config.speech_recognition_language = self._from_lang
        # Enable dictation mode
        speech_config.enable_dictation = True
        # Set the profanity option to medium
        speech_config.set_profanity = speechsdk.ProfanityOption(2)
        # Set the output format to simple JSON
        speech_config.output_format = speechsdk.OutputFormat(0)

        # Configure the audio input
        audio_config = speechsdk.audio.AudioConfig(filename=self._media_path)

        # Create a translation recognizer with the configured settings
        speech_recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=speech_config,
            audio_config=audio_config,
        )

        # Define the event handler for when speech is recognized
        def on_recognized(evt):
            # Extract the result data from the recognized
            print("SUCCESS")
            data = VideoSerializer.ResultSerializer({"result": json.loads(evt.result.json)}).data["result"]
            translation = data["Translation"]["Translations"][0]["Text"]
            words = data["Words"]
            # Map the translations to the corresponding audio words
            self.result.extend(map_translations_to_audio_words(translation, words))

        # Define the event handler for when speech recognition is canceled
        def on_canceled(evt: speechsdk.translation.TranslationRecognitionCanceledEventArgs):
            print("CANCELED", evt.cancellation_details)

        # Define the event handler for when the recognition session is stopped
        def stop_cb(evt):
            print(f"CLOSING on {evt}")
            # Stop continuous recognition and mark the process as done
            speech_recognizer.stop_continuous_recognition()
            nonlocal done
            done = True

        # Connect the event handlers to the recognizer events
        speech_recognizer.recognized.connect(on_recognized)
        speech_recognizer.canceled.connect(on_canceled)
        speech_recognizer.session_stopped.connect(stop_cb)

        # Start continuous recognition
        speech_recognizer.start_continuous_recognition()
        done = False

        # Wait until the recognition process is done
        while not done:
            time.sleep(0.5)

        copy = self.result.copy()
        self.result = []
        # Return the final result
        return copy

    def transcribe(self) -> list[dict]:
        self.result = []
        print("TRANSCRIBING")
        # Create a SpeechConfig object with the provided service key and endpoint
        speech_config = speechsdk.transcription.SpeechConfig(subscription=SERVICE_KEY, endpoint=ENDPOINT)

        # Enable word-level timestamps in the transcription
        speech_config.request_word_level_timestamps()

        # Set the speech recognition language to the language specified in the `from_lang` attribute
        speech_config.speech_recognition_language = self._from_lang

        # Enable dictation mode for continuous speech recognition
        speech_config.enable_dictation = True

        # Set the profanity option to filter out offensive language
        speech_config.set_profanity = speechsdk.ProfanityOption(2)

        # Set the output format to JSON
        speech_config.output_format = speechsdk.OutputFormat(0)

        # Create an AudioConfig object with the provided media file path
        audio_config = speechsdk.audio.AudioConfig(filename=self._media_path)

        # Create a SpeechRecognizer object with the SpeechConfig and AudioConfig objects
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config,
        )

        # Define a callback function to handle recognized speech
        def on_recognized(evt: speechsdk.SpeechRecognitionEventArgs):
            # Print "SUCCESS" when speech is recognized
            print("SUCCESS")
            # Access the recognized words from the JSON result and assign them to the `result` attribute
            data = VideoSerializer.ResultSerializer({"result": json.loads(evt.result.json)}).data["result"]["NBest"][
                0
            ]["Words"]
            self.result.extend(to_representation(data))

        # Define a callback function to handle canceled speech recognition
        def on_canceled(evt: speechsdk.SpeechRecognitionCanceledEventArgs):
            # Print "CANCELED" and the cancellation details when speech recognition is canceled
            print("CANCELED", evt.cancellation_details)

        # Define a callback function to handle stopping continuous recognition
        def stop_cb(evt):
            # Print "CLOSING" and the event when continuous recognition is stopped
            print(f"CLOSING on {evt}")

            # Stop continuous speech recognition
            speech_recognizer.stop_continuous_recognition()
            # Set the `done` flag to True to exit the while loop
            nonlocal done
            done = True

        # Connect the on_recognized callback function to the recognized event
        speech_recognizer.recognized.connect(on_recognized)

        # Connect the on_canceled callback function to the canceled event
        speech_recognizer.canceled.connect(on_canceled)

        # Connect the stop_cb callback function to the session_stopped event
        speech_recognizer.session_stopped.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        # Set the `done` flag to False to indicate that speech recognition is still in progress
        done = False

        # Wait until speech recognition is done
        while not done:
            time.sleep(0.5)

        copy = self.result.copy()
        self.result = []
        # Return the recognized result
        return copy
