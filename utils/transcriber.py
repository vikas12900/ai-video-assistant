import whisper

model = whisper.load_model("base")

def transcribe_audio(audio_path):

    result = model.transcribe(audio_path)

    detected = result["language"]

    # Only allow English or Hindi
    if detected not in ["en", "hi"]:

        # Fallback: assume Hindi
        result = model.transcribe(
            audio_path,
            language="hi"
        )

    return result