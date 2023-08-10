import openai
# from django.conf import settings

# OPEN_API_KEY = settings.OPEN_API_KEY
# Initialize your OpenAI API key
openai.api_key = "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"

def transcribe_media(media_file_path):
    try:
        # Read the media file
        with open(media_file_path, 'rb') as f:
            # media_file_content = f.read()

            # Use OpenAI's Whisper API for speech-to-text transcription
            transcription_result = openai.Audio.transcribe(
                model="whisper-1",
                file=f,
            )

            # Extract the transcribed text from the API response
            transcription_text = transcription_result['choices'][0]['text']

        return transcription_text

    except FileNotFoundError:
        print(f"File not found at the given path: {media_file_path}")
    except openai.error.OpenAIError as e:
        print(f"Error with the OpenAI API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

# # Example usage:
media_file_path = "./Burna-Boy-Kilometre-(TrendyBeatz.com).mp3"  # Replace this with the actual media file path
transcribed_text = transcribe_media(media_file_path)
print(transcribed_text)
