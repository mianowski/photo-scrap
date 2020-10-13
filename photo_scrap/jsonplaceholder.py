from __future__ import annotations  # for type hints of typed lists

import os
import itertools
import concurrent.futures
from tqdm import tqdm
from dataclasses import dataclass

from .rest_client import RestClient
from .csv_writer import CsvWriter


def split_even(l: list, parts: int):
    size = len(l)//parts + 1 if len(l) % parts else len(l)//parts
    return [l[i*size: (i+1)*size] for i in range(parts)]


@dataclass
class UsersList():
    users: list[dict]

    def to_csv(self, csv_path: str = 'users.csv'):
        return CsvWriter.to_csv(self.users, csv_path, ['id', 'address.city', 'address.geo.lat', 'address.geo.lng', 'address.street', 'address.suite', 'address.zipcode', 'company.bs', 'company.catchPhrase', 'company.name', 'email', 'name', 'phone', 'username', 'website'])


@dataclass
class AlbumsList():
    albums: list[dict]

    def get_album_ids(self):
        return [album['id'] for album in self.albums if 'id' in album]

    def to_csv(self, csv_path: str = 'albums.csv'):
        return CsvWriter.to_csv(self.albums, csv_path, ['user_id', 'id', 'title'])


@dataclass
class PhotosList():
    photos: list[dict]

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
        return [PhotosList(i) for i in split_even(self.photos, parts)]


class JphScrapper():
    def __init__(self, user_ids: list = [], threads: int = 4):
        self.threads = threads

    @staticmethod
    def _get_users_list_single(user_ids: list[int]) -> list[dict]:
        return [RestClient.getUser(user_id) for user_id in user_ids]

    @staticmethod
    def get_users_list(user_ids: list[int], threads: int) -> UsersList:
        fun = JphScrapper._get_users_list_single
        results = JphScrapper.parallelize(user_ids, threads, fun)
        return UsersList(results)

    @staticmethod
    def _get_album_photos_single(album_ids: list[int]) -> list[dict]:
        return list(itertools.chain.from_iterable([RestClient.getAlbumPhotos(album_id) for album_id in album_ids]))

    @staticmethod
    def get_album_photos(user_ids: list[int], threads: int) -> PhotosList:
        fun = JphScrapper._get_album_photos_single
        results = JphScrapper.parallelize(user_ids, threads, fun)
        return PhotosList(results)

    @staticmethod
    def _get_user_albums_single(user_ids: list[int]) -> list[dict]:
        return list(itertools.chain.from_iterable([RestClient.get_user_albums(user_id) for user_id in user_ids]))

    @staticmethod
    def get_user_albums(user_ids: list[int], threads: int) -> AlbumsList:
        fun = JphScrapper._get_user_albums_single
        results = JphScrapper.parallelize(user_ids, threads, fun)
        return AlbumsList(results)

    @staticmethod
    def parallelize(args, threads, fun):
        split_args = split_even(args, threads)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(fun, ids)
                       for ids in split_args]
        results = list(itertools.chain.from_iterable(
            [f.result() for f in futures]))
        return results
