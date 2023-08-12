import whisper

model = whisper.load_model(
    "small",
)

result = model.transcribe("./ar.mp3", task="transcribe")
print(result)

# # load audio and pad/trim it to fit 30 seconds
# audio = whisper.load_audio("./Burna-Boy-Kilometre-(TrendyBeatz.com).mp3")
# audio = whisper.pad_or_trim(audio)

# # make log-Mel spectrogram and move to the same device as the model
# mel = whisper.log_mel_spectrogram(audio).to(model.device)

# # detect the spoken language
# _, probs = model.detect_language(mel)
# print(f"Detected language: {max(probs, key=probs.get)}")

# # decode the audio
# options = whisper.DecodingOptions()
# result = whisper.decode(model, mel, options)

# # print the recognized text
# print(result.text)
