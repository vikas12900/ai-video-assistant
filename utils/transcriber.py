from faster_whisper import WhisperModel
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = WhisperModel(
    "base",
    device=device,
    compute_type="float16" if device == "cuda" else "int8"
)

def transcribe_audio(audio_path):

    segments, info = model.transcribe(audio_path)
    print(type(segments))
    print(type(info))
    segments = list(segments)

    detected = info.language

    if detected not in ["en", "hi"]:

        segments, info = model.transcribe(
            audio_path,
            language="hi"
        )

    return {
    "language": info.language,
    "text": " ".join(segment.text for segment in segments),
    "segments": [
        {
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        }
        for segment in segments
    ]
}