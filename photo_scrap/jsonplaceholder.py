from __future__ import annotations  # for type hints of typed lists
from .rest_client import RestClient
from .csv_writer import CsvWriter
import os
import itertools
from tqdm import tqdm


class UsersList():
    def __init__(self, users: list[dict]):
        self.users = users

    def to_csv(self, csv_path: str = 'users.csv'):
        return CsvWriter.to_csv(self.users, csv_path, ['id', 'address.city', 'address.geo.lat', 'address.geo.lng', 'address.street', 'address.suite', 'address.zipcode', 'company.bs', 'company.catchPhrase', 'company.name', 'email', 'name', 'phone', 'username', 'website'])


class AlbumsList():
    def __init__(self, albums: list[dict]):
        self.albums = albums

    def get_album_ids(self):
        return [album['id'] for album in self.albums if 'id' in album]

    def to_csv(self, csv_path: str = 'albums.csv'):
        return CsvWriter.to_csv(self.albums, csv_path, ['user_id', 'id', 'title'])


class PhotosList():
    def __init__(self, photos: list[dict]):
        self.photos = photos

    def add_file_path_each_photo(self, photos_dir: str):
        for photo in self.photos:
            photo['file_path'] = os.path.join(
                photos_dir, photo['url'].split('/')[-1]+'.png')
        return self.photos

    def to_csv(self, csv_path: str = 'photos.csv'):
        return CsvWriter.to_csv(self.photos, csv_path, ['albumId', 'id', 'title',
                                                        'url',
                                                        'thumbnailUrl',
                                                        'file_path'])

    def download_photos(self):
        for photo in tqdm(self.photos):
            if (photo['url'] and photo['file_path']):
                RestClient.downloadPhoto(
                    photo['thumbnailUrl'], photo['file_path'])

    def split(self, parts):
        size = len(self.photos)//parts + 1
        return [PhotosList(self.photos[i:i + size]) for i in range(0, len(self.photos), size)]


class JphScrapper():
    def __init__(self, user_ids: list = [], threads: int = 1):
        self.threads = threads

    @ staticmethod
    def get_album_photos(album_ids: list[int]) -> PhotosList:
        return PhotosList(list(itertools.chain.from_iterable([RestClient.getAlbumPhotos(album_id) for album_id in album_ids])))

    @staticmethod
    def get_users_list(user_ids: list[int]) -> UsersList:
        return UsersList([RestClient.getUser(user_id) for user_id in user_ids])

    @staticmethod
    def get_user_albums(user_ids: list[int]) -> AlbumsList:
        return AlbumsList(list(itertools.chain.from_iterable([RestClient.get_user_albums(user_id) for user_id in user_ids])))
