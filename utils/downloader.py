import yt_dlp

def download_audio(url):

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "data/audio.%(ext)s",
        "ffmpeg_location": r"C:\Users\Vikas\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128",
        }],
    }

    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ydl.download([url])

    return "data/audio.mp3"