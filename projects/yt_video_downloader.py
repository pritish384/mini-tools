from pytube import YouTube


def get_video_download_url(url):
    try:
        youtube = YouTube(url)
        video = youtube.streams.get_highest_resolution()
        return video.url
    except Exception as e:
        return print(e)