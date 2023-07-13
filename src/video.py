from googleapiclient.discovery import build
from pprint import pprint
import os

class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        # YOUTUBE_API_KEY в переменных окружения
        api_key = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.title = video_response['items'][0]['snippet']['title']
        self.url = 'https://youtu.be/' + self.video_id
        self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
        self.like_count = int(video_response['items'][0]['statistics']['likeCount'])


    def __str__(self):
        return self.title




class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

