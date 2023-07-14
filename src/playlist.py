from googleapiclient.discovery import build
import os
import isodate
import datetime


class PlayList:
    YT_OBJ = None  # YT object

    def __init__(self, playlist_id):
        self._playlist_id = playlist_id
        self._url = 'https://www.youtube.com/playlist?list=' + playlist_id

        api_key = os.getenv('YOUTUBE_API_KEY')  # YOUTUBE_API_KEY в переменных окружения
        self.__class__.YT_OBJ = build('youtube', 'v3', developerKey=api_key)

        # узнаём id канала, которому принадлежит плейлист
        playlist_info = self.__class__.YT_OBJ.playlistItems().list(playlistId=playlist_id,
                                                                   part='contentDetails, snippet',
                                                                   maxResults=50,
                                                                   ).execute()
        channel_id = playlist_info['items'][0]['snippet']['channelId']

        # узнаём название плейлиста
        playlists = self.__class__.YT_OBJ.playlists().list(channelId=channel_id,
                                                           part='contentDetails,snippet',
                                                           maxResults=50,
                                                           ).execute()
        self._title = [channel['snippet']['title'] for channel in playlists['items'] if channel['id'] == playlist_id][0]

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def total_duration(self):
        """Возвращает общую длительность видео в плейлисте в формате timedelta"""
        playlist_videos = self.__class__.YT_OBJ.playlistItems().list(playlistId=self._playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.__class__.YT_OBJ.videos().list(part='contentDetails,statistics',
                                                             id=','.join(video_ids)
                                                             ).execute()

        time_cnt = datetime.timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_cnt += duration

        return time_cnt

    def show_best_video(self):
        """Возвращает ссылку на видео в плейлисте с максимальным количеством лайков"""
        playlist_videos = self.__class__.YT_OBJ.playlistItems().list(playlistId=self._playlist_id,
                                                                     part='contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.__class__.YT_OBJ.videos().list(part='contentDetails,statistics',
                                                             id=','.join(video_ids)
                                                             ).execute()

        best_video = max(video_response['items'], key=lambda video: int(video['statistics']['likeCount']))
        return f"https://youtu.be/{best_video['id']}"
