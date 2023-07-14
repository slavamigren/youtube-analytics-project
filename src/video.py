from googleapiclient.discovery import build
import os


class Video:

    YT_OBJ = None   # YT object

    def __init__(self, video_id):
        self._video_id = video_id
        # YOUTUBE_API_KEY в переменных окружения
        api_key = os.getenv('YOUTUBE_API_KEY')
        self.__class__.YT_OBJ = build('youtube', 'v3', developerKey=api_key)
        video_response = self.__class__.YT_OBJ.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        try:
            self._title = video_response['items'][0]['snippet']['title']
            self._url = 'https://youtu.be/' + self._video_id
            self._view_count = int(video_response['items'][0]['statistics']['viewCount'])
            self._like_count = int(video_response['items'][0]['statistics']['likeCount'])
        except:
            self._title = self._url = self._view_count = self._like_count = None

    def __str__(self):
        return self.title

    @property
    def url(self):
        return self._url

    @property
    def video_id(self):
        return self._video_id

    @property
    def title(self):
        return self._title

    @property
    def view_count(self):
        return self._view_count

    @property
    def like_count(self):
        return self._like_count


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self._playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self._playlist_id
