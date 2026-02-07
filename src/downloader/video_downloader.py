import logging
import random
import yt_dlp

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

youtube_channel = "https://www.youtube.com/@TheGarschive/shorts"

class YouTubeDownloaderHelper:

    info_opts = {
        "extract_flat": True, 
    }

    download_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",      
        "outtmpl": "downloads/%(title)s.%(ext)s",
    }

    def __init__(self, channel=youtube_channel, debug=False):
        self._channel = channel
        self._selected_video = ""
        self._video_path = "" 
        self._video_info = {}
        
        if debug:
            logger.setLevel(logging.DEBUG)

    def get_random_video_from_channel(self) -> None:
        #logger.debug("Starting info extraction.")
        with yt_dlp.YoutubeDL(self.info_opts) as ydl:
            channel_info = ydl.extract_info(self._channel, download=False)
        
        # this was found just by printing output until I found the shorts
        shorts = channel_info["entries"] 

        self._selected_video = random.choice(shorts)["url"]

    def get_video_information(self) -> None:
        if self._selected_video == "":
            logger.warning("No video has been selected.")
            return
        
        with yt_dlp.YoutubeDL(self.info_opts) as ydl:
            video_info = ydl.extract_info(self._selected_video, download=False)
        
        self._video_info["upload_date"] = video_info["upload_date"]

    def download_video(self) -> None:
        if self._selected_video == "":
            logger.warning("No video has been selected.")
            return
        
        with yt_dlp.YoutubeDL(self.download_opts) as ydl:
            ydl.download([self._selected_video])
        

if __name__ == "__main__":
    ytdownloader = YouTubeDownloaderHelper(debug=True)

    ytdownloader.get_random_video_from_channel()
    ytdownloader.get_video_information()
    ytdownloader.download_video()
