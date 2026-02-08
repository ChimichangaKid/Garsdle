import logging
import random
import yt_dlp
import json
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

youtube_channel = "https://www.youtube.com/@TheGarschive/shorts"
data_dir = r"downloads\daily_info.json"

class YouTubeDownloaderHelper:

    info_opts = {
        "extract_flat": True, 
    }

    download_opts = {
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "outtmpl": "downloads/daily.mp4",
        "force_overwrites": True,
        "nopart": True,
        "continuedl": False,
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

        date = video_info["upload_date"]

        self._video_info["upload_date"] = date
        self.convert_date_to_int(date)

        with open(data_dir, 'w', encoding="utf-8") as f:
            json.dump(self._video_info, f, ensure_ascii=False, indent=4)

    def download_video(self) -> None:
        if self._selected_video == "":
            logger.warning("No video has been selected.")
            return

        if os.path.exists("downloads/daily_video.mp4"):
            os.remove("downloads/daily_video.mp4")
        
        with yt_dlp.YoutubeDL(self.download_opts) as ydl:
            ydl.download([self._selected_video])

            os.rename("downloads/daily.mp4", "downloads/daily_video.mp4")

    def convert_date_to_int(self, value: str):
        year = int(value[:4])
        month = int(value[4:6])

        print(f"year {year}, month {month}")

        self._video_info["upload_date_int"] = 12 * (year - 2023) + month

if __name__ == "__main__":
    ytdownloader = YouTubeDownloaderHelper(debug=True)

    ytdownloader.get_random_video_from_channel()
    ytdownloader.get_video_information()
    ytdownloader.download_video()
