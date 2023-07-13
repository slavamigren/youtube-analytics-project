import json
import os
from googleapiclient.discovery import build
import isodate


class Channel:
    """Класс для ютуб-канала"""

    YT_OBJ = None # YT object

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        # YOUTUBE_API_KEY в переменных окружения
        api_key = os.getenv('YOUTUBE_API_KEY')
        # создает специальный объект для работы с API
        self.__class__.YT_OBJ = build('youtube', 'v3', developerKey=api_key)
        # загрузить инфо о канале
        info = self.__class__.YT_OBJ.channels().list(id=channel_id, part='snippet,statistics').execute()

        self._channel_id = info['items'][0]['id']    # id of the channel
        self._title = info['items'][0]['snippet']['title']    # title of the channel
        self._description = info['items'][0]['snippet']['description']    # description of the channel
        self._url = 'https://www.youtube.com/channel/' + info['items'][0]['snippet']['customUrl']    # url of the channel
        self._subscriber_count = info['items'][0]['statistics']['subscriberCount']    # amount of subscribers
        self._video_count = info['items'][0]['statistics']['videoCount']    # amount of videos
        self._view_count = info['items'][0]['statistics']['viewCount']    # amount of views


    @property
    def channel_id(self):
        return self._channel_id


    @property
    def title(self):
        return self._title


    @property
    def description(self):
        return self._description


    @property
    def url(self):
        return self._url


    @property
    def subscriber_count(self):
        return self._subscriber_count


    @property
    def video_count(self):
        return self._video_count


    @property
    def view_count(self):
        return self._view_count


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        info = self.__class__.YT_OBJ.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(info, indent=2, ensure_ascii=False))


    @classmethod
    def get_service(cls):
        """возвращает объект для работы с API вне класса"""
        return cls.YT_OBJ


    def to_json(self, filename):
        """выгружает атрибуты класса в json файл"""
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file, indent=2)



if __name__ == '__main__':
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
#    moscowpython.print_info()
    print(moscowpython.channel_id)
    print(moscowpython.title)
    print(moscowpython.description)
    print(moscowpython.url)
    print(moscowpython.subscriber_count)
    print(moscowpython.video_count)
    print(moscowpython.view_count)
    print(moscowpython.get_service())
    moscowpython.to_json('moscowpython.json')
