import whisper

model = whisper.load_model(
    "small",
)

result = model.transcribe("./ar.mp3", task="transcribe")
