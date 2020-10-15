from __future__ import annotations  # for type hints of typed lists
import unittest
import sys
import os
import csv
import random

from photo_scrap import scrapper as scr
from photo_scrap.rest_client import RestClient


class UsersListTest(unittest.TestCase):
    users = [
        {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {
                "street": "Kulas Light",
                "suite": "Apt. 556",
                "city": "Gwenborough",
                "zipcode": "92998-3874",
                "geo": {
                    "lat": "-37.3159",
                    "lng": "81.1496"
                }
            },
            "phone": "1-770-736-8031 x56442",
            "website": "hildegard.org",
            "company": {
                "name": "Romaguera-Crona",
                "catchPhrase": "Multi-layered client-server neural-net",
                "bs": "harness real-time e-markets"
            }
        },
        {
            "id": 2,
            "name": "Ervin Howell",
            "username": "Antonette",
            "email": "Shanna@melissa.tv",
            "address": {
                "street": "Victor Plains",
                "suite": "Suite 879",
                "city": "Wisokyburgh",
                "zipcode": "90566-7771",
                "geo": {
                    "lat": "-43.9509",
                    "lng": "-34.4618"
                }
            },
            "phone": "010-692-6593 x09125",
            "website": "anastasia.net",
            "company": {
                "name": "Deckow-Crist",
                "catchPhrase": "Proactive didactic contingency",
                "bs": "synergize scalable supply-chains"
            }
        }
    ]

    def setUp(self):
        self.filename = 'test_users.csv'
        self.users_list = scr.UsersList(
            UsersListTest.users)

    def test_to_csv_writes_file(self):
        self.assertTrue(self.users_list.to_csv(self.filename))
        self.assertTrue(os.path.exists(self.filename))

    def tearDown(self):
        os.remove(self.filename)


class AlbumListTest(unittest.TestCase):
    albums = [{"userId": 3, "id": 21, "title": "repudiandae voluptatem optio est consequatur rem in temporibus et"},
              {"userId": 3, "id": 22, "title": "et rem non provident vel ut"},
              {"userId": 3, "id": 23,
               "title": "incidunt quisquam hic adipisci sequi"},
              {"userId": 3, "id": 24, "title": "dolores ut et facere placeat"},
              {"userId": 3, "id": 25,
               "title": "vero maxime id possimus sunt neque et consequatur"},
              {"userId": 3, "id": 26, "title": "quibusdam saepe ipsa vel harum"},
              {"userId": 3, "id": 27, "title": "id non nostrum expedita"},
              {"userId": 3, "id": 28,
               "title": "omnis neque exercitationem sed dolor atque maxime aut cum"},
              {"userId": 3, "id": 29,
               "title": "inventore ut quasi magnam itaque est fugit"},
              {"userId": 3, "id": 30, "title": "tempora assumenda et similique odit distinctio error"}]

    def setUp(self):
        self.album_list = scr.AlbumsList(
            AlbumListTest.albums)

    def test_get_album_ids_returns_correct_list(self):
        self.assertEqual(
            self.album_list.get_album_ids(), list(range(21, 31))
        )

    def test_to_csv_writes_file(self):
        filename = 'test_albums.csv'
        self.assertTrue(self.album_list.to_csv(filename))
        self.assertEqual(os.path.exists(filename), True)
        os.remove(filename)


class PhotosListTest(unittest.TestCase):
    photos = [
        {
            "album_id": 1,
            "id": 1,
            "title": "accusamus beatae ad facilis cum similique qui sunt",
            "url": "https://via.placeholder.com/600/92c952",
            "thumbnailUrl": "https://via.placeholder.com/150/92c952"
        },
        {
            "album_id": 1,
            "id": 2,
            "title": "reprehenderit est deserunt velit ipsam",
            "url": "https://via.placeholder.com/600/771796",
            "thumbnailUrl": "https://via.placeholder.com/150/771796"
        }
    ]
    photos_dir = 'photos'

    def setUp(self):
        self.filename = 'test_photos.csv'
        scr.PhotosList(PhotosListTest.photos).add_file_path_each_photo(PhotosListTest.photos_dir).to_csv(
            self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_to_csv_writes_file(self):
        self.assertEqual(os.path.exists(self.filename), True)

    def test_to_csv_writes_file_path_column(self):
        with open(self.filename, newline='') as csvfile:
            r = csv.DictReader(csvfile)
            self.assertTrue('file_path' in next(r).keys())

    def test_to_csv_writes_file_path_correctly(self):
        with open(self.filename, newline='') as csvfile:
            r = csv.DictReader(csvfile)
            test_photo = next(r)
        self.assertEqual(test_photo['file_path'],
                         PhotosListTest.photos_dir+'/92c952.png')


class PhotoScrapperTest(unittest.TestCase):
    class FakeRestClient(RestClient):
        @classmethod
        def get_user(cls, user_id: int) -> dict:
            return {
                "id": user_id,
                "name": "Leanne Graham",
                "username": "Bret",
                "email": "Sincere@april.biz",
                "address": {
                    "street": "Kulas Light",
                    "suite": "Apt. 556",
                    "city": "Gwenborough",
                    "zipcode": "92998-3874",
                    "geo": {
                        "lat": "-37.3159",
                        "lng": "81.1496"
                    }
                }
            }

        @ classmethod
        def get_user_albums(cls, user_id: int) -> list[dict]:
            return [
                {"userId": user_id, "id": 10*user_id+1,
                    "title": "repudiandae voluptatem optio est consequatur rem in temporibus et"},
                {"userId": user_id, "id": 10*user_id+2,
                    "title": "et rem non provident vel ut"},
                {"userId": user_id, "id": 10*user_id+3,
                    "title": "incidunt quisquam hic adipisci sequi"},
            ]

        @ classmethod
        def get_album_photos(cls, album_id: int) -> list[dict]:
            return [
                {
                    "album_id": album_id,
                    "id": 10*album_id+1,
                    "title": "accusamus beatae ad facilis cum similique qui sunt",
                    "url": "https://via.placeholder.com/600/92c952",
                    "thumbnailUrl": "https://via.placeholder.com/150/92c952"
                },
                {
                    "album_id": album_id,
                    "id": 10*album_id+2,
                    "title": "reprehenderit est deserunt velit ipsam",
                    "url": "https://via.placeholder.com/600/771796",
                    "thumbnailUrl": "https://via.placeholder.com/150/771796"
                }
            ]
    scrapper = scr.PhotoScrapper(FakeRestClient)
    threads = 3

    def test_get_user_list(self):
        user_ids = [1, 2, 3]
        users_list = self.scrapper.get_users_list(user_ids, self.threads)
        self.assertEqual(
            sorted([user["id"] for user in users_list.users]), sorted(user_ids))

    def test_get_user_albums(self):
        user_ids = [1, 2]
        albums_list = self.scrapper.get_user_albums(user_ids, self.threads)
        self.assertEqual(sorted([album["id"] for album in albums_list.albums]), [
            11, 12, 13, 21, 22, 23])

    def test_get_album_photos(self):
        album_ids = [7, 8]
        photos_list = self.scrapper.get_album_photos(album_ids, self.threads)
        self.assertEqual(sorted([photo["id"] for photo in photos_list.photos]), [
            71, 72, 81, 82])

    def test_get_album_photos_threads_count_unimportant(self):
        album_ids = [7, 8]
        photos_list1 = self.scrapper.get_album_photos(album_ids, self.threads)
        photos_list2 = self.scrapper.get_album_photos(
            album_ids, random.randint(1, 10))
        self.assertEqual(sorted([photo["id"] for photo in photos_list1.photos]), sorted(
            [photo["id"] for photo in photos_list2.photos]))


if __name__ == '__main__':
    unittest.main()
