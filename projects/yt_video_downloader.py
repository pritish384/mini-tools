from pytube import YouTube

def get_video_download_url(url):    
    youtube = YouTube(url)
    video = youtube.streams.get_highest_resolution()
    return video.url