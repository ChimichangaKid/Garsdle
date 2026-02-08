import logging
import random
import yt_dlp
import json

CURRENT_NUMBER_OF_VIDEOS = 20

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

youtube_channel = "https://www.youtube.com/@TheGarschive/shorts"
data_dir = r"app\daily\daily_info.json"


class YouTubeDownloaderHelper:

    info_opts = {
        "extract_flat": True, 
        "skip_download": True,
        "playlistend": CURRENT_NUMBER_OF_VIDEOS,
    }

    def __init__(self, channel=youtube_channel, debug=False):
        self._channel = channel
        self._selected_video = ""
        self._video_path = "" 
        self._video_info = {}
        with open(r"app\daily\video_list.json", "r") as f:
            self._video_list = json.load(f)
        
        if debug:
            logger.setLevel(logging.DEBUG)

    def get_random_video_from_channel(self) -> None:
        #logger.debug("Starting info extraction.")

        random_video_info = random.choice(self._video_list)
        with open(data_dir, 'w', encoding="utf-8") as f:
            json.dump(random_video_info, f, ensure_ascii=False, indent=4)

    @staticmethod
    def convert_date_to_int(value: str):
        year = int(value[:4])
        month = int(value[4:6])
        return 12 * (year - 2023) + month

    def get_data(self):
        with yt_dlp.YoutubeDL(self.info_opts) as ydl:
            try:
                info_dict = ydl.extract_info(self._channel, download=False)
                # For a playlist/channel, entries contains all videos
                for entry in info_dict.get("entries", []):

                    info = ydl.extract_info(entry["url"], download=False)
                    video_data = {
                        "embed_url": f"https://www.youtube.com/embed/{info.get('id')}?rel=0&modestbranding=1&autoplay=0&mute=1&controls=1",
                        "upload_date": info.get("upload_date"),
                        "upload_date_int": self.convert_date_to_int(info.get("upload_date")),
                    }
                    self._video_list.append(video_data)
                    with open("daily/video_list.json", "w") as f:
                        json.dump(self._video_list, f, indent=4)
            except Exception as e:
                print(f"Error fetching channel info: {e}")

if __name__ == "__main__":
    ytdownloader = YouTubeDownloaderHelper(debug=True)

    ytdownloader.get_random_video_from_channel()
