import logging
import random
import yt_dlp
import json
import os
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

youtube_channel = "https://www.youtube.com/@TheGarschive/shorts"
data_dir = r"downloads\daily_info.json"

class YouTubeDownloaderHelper:

    info_opts = {
        "extract_flat": True, 
        "skip_download": True,
        "playlistend": 200,
    }

    # download_opts = {
    #     "format": "bv*+ba/b",
    #     "merge_output_format": "mp4",
    #     "outtmpl": "downloads/daily.mp4",
    #     "force_overwrites": True,
    #     "nopart": True,
    #     "continuedl": False,
    # }

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
        match = re.search(r"shorts/([a-zA-Z0-9_-]+)", self._selected_video)
        
    
        video_id = match.group(1)
        embed_url = f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&autoplay=1&mute=1&controls=1"

        self._video_info["url"] = embed_url

    def get_video_information(self) -> None:
        if self._selected_video == "":
            logger.warning("No video has been selected.")
            return
        
        with yt_dlp.YoutubeDL(self.info_opts) as ydl:
            video_info = ydl.extract_info(self._selected_video, download=False)

        date = video_info["upload_date"]

        self._video_info["upload_date"] = date
        self.convert_date_to_int(date)

        with open(data_dir, 'w', encoding="utf-8") as f:
            json.dump(self._video_info, f, ensure_ascii=False, indent=4)

    def convert_date_to_int(self, value: str):
        year = int(value[:4])
        month = int(value[4:6])



        self._video_info["upload_date_int"] = 12 * (year - 2023) + month

if __name__ == "__main__":
    ytdownloader = YouTubeDownloaderHelper(debug=True)

    ytdownloader.get_random_video_from_channel()
    # ytdownloader.get_video_information()
    # ytdownloader.download_video()
