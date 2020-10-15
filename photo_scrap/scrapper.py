from __future__ import annotations  # for type hints of typed lists

import os
import itertools

from tqdm import tqdm
from dataclasses import dataclass

from .rest_client import RestClient, download_photo
from .csv_writer import to_csv
from .helpers import parallelize


@ dataclass
class UsersList():
    users: list[dict]

    def to_csv(self, csv_path: str = 'users.csv'):
        return to_csv(self.users, csv_path, ['id', 'address.city', 'address.geo.lat', 'address.geo.lng', 'address.street', 'address.suite', 'address.zipcode', 'company.bs', 'company.catchPhrase', 'company.name', 'email', 'name', 'phone', 'username', 'website'])


@ dataclass
class AlbumsList():
    albums: list[dict]

    def get_album_ids(self):
        return [album['id'] for album in self.albums if 'id' in album]

    def to_csv(self, csv_path: str = 'albums.csv'):
        return to_csv(self.albums, csv_path, ['user_id', 'id', 'title'])


@ dataclass
class PhotosList():
    photos: list[dict]

    @staticmethod
    def path_from_url(photos_dir: str, url: str):
        return os.path.join(photos_dir, url.split('/')[-1]+'.png')

    def add_file_path_each_photo(self, photos_dir: str):
        for photo in self.photos:
            photo['file_path'] = self.path_from_url(
                photos_dir, photo['url'])
        return self

    def to_csv(self, csv_path: str = 'photos.csv'):
        return to_csv(self.photos, csv_path, ['albumId', 'id', 'title',
                                              'url',
                                              'thumbnailUrl',
                                              'file_path'])

    @ staticmethod
    def _download_photos_single(photos):
        to_retry = []
        for photo in tqdm(photos):
            if (photo['url'] and photo['file_path']):
                if not download_photo(photo['url'], photo['file_path']):
                    to_retry.append(photo)
        return to_retry

    def download_photos(self, threads_count, max_retries: int = 3):
        print('Downloading photos by {} threads'.format(threads_count))
        to_download = self.photos
        retries = 0
        while (to_download and retries <= max_retries):
            retries += 1
            to_download = parallelize(
                to_download, threads_count, self._download_photos_single)
        print('Downolading finished')


class PhotoScrapper():
    def __init__(self, rest_client):
        self.rest_client = rest_client

    def _get_users_list_single(self, user_ids: list[int]) -> list[dict]:
        return [self.rest_client.get_user(user_id) for user_id in user_ids]

    def _get_user_albums_single(self, user_ids: list[int]) -> list[dict]:
        return list(itertools.chain.from_iterable([self.rest_client.get_user_albums(user_id) for user_id in user_ids]))

    def _get_album_photos_single(self, album_ids: list[int]) -> list[dict]:
        return list(itertools.chain.from_iterable([self.rest_client.get_album_photos(album_id) for album_id in album_ids]))

    def get_users_list(self, user_ids: list[int], threads: int) -> UsersList:
        return UsersList(parallelize(user_ids, threads, self._get_users_list_single))

    def get_user_albums(self, user_ids: list[int], threads: int) -> AlbumsList:
        return AlbumsList(parallelize(user_ids, threads, self._get_user_albums_single))

    def get_album_photos(self, user_ids: list[int], threads: int) -> PhotosList:
        return PhotosList(parallelize(user_ids, threads, self._get_album_photos_single))
