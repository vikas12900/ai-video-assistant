import yt_dlp

def download_audio(url):

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "data/audio.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "128",
    }],
    }
    

    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ydl.download([url])

    return "data/audio.mp3"