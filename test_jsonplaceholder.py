from photo_scrap import jsonplaceholder as jph

import unittest
import sys
import os
import csv


class SplitEvenTest(unittest.TestCase):
    def test_correctness_for_indivisible(self):
        self.assertEquals(jph.split_even(
            [0, 1, 2, "three", {4}], 3), [[0, 1], [2, "three"], [{4}]])

    def test_correctness_for_divisible(self):
        self.assertEquals(jph.split_even(
            [0, 1, 2, 3, 4, 5], 3), [[0, 1], [2, 3], [4, 5]])

    def test_too_short_list_is_split_to_correct_number_of_parts(self):
        self.assertEquals(jph.split_even(
            [0, 1], 3), [[0], [1], []])

    def test_empty_list_is_split_to_empty_lists(self):
        self.assertEquals(jph.split_even(
            [], 3), [[], [], []])

    def test_negative_parts_count_result_in_empty_result(self):
        self.assertEquals(jph.split_even(
            [1, 2, 3], -1), [])


class AlbumListTest(unittest.TestCase):
    albums = [{'userId': 3, 'id': 21, 'title': 'repudiandae voluptatem optio est consequatur rem in temporibus et'},
              {'userId': 3, 'id': 22, 'title': 'et rem non provident vel ut'},
              {'userId': 3, 'id': 23,
               'title': 'incidunt quisquam hic adipisci sequi'},
              {'userId': 3, 'id': 24, 'title': 'dolores ut et facere placeat'},
              {'userId': 3, 'id': 25,
               'title': 'vero maxime id possimus sunt neque et consequatur'},
              {'userId': 3, 'id': 26, 'title': 'quibusdam saepe ipsa vel harum'},
              {'userId': 3, 'id': 27, 'title': 'id non nostrum expedita'},
              {'userId': 3, 'id': 28,
               'title': 'omnis neque exercitationem sed dolor atque maxime aut cum'},
              {'userId': 3, 'id': 29,
               'title': 'inventore ut quasi magnam itaque est fugit'},
              {'userId': 3, 'id': 30, 'title': 'tempora assumenda et similique odit distinctio error'}]

    def test_get_album_ids_returns_correct_list(self):
        album_list = jph.AlbumsList(
            AlbumListTest.albums)
        self.assertEqual(album_list.get_album_ids(), list(range(21, 31)))

    def test_to_csv_writes_file(self):
        filename = 'test_albums.csv'
        album_list = jph.AlbumsList(
            AlbumListTest.albums)
        self.assertTrue(album_list.to_csv(filename))
        self.assertEquals(os.path.exists(filename), True)
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

    def test_to_csv_writes_file(self):
        filename = 'test_photos.csv'
        jph.PhotosList(PhotosListTest.photos).to_csv(filename)
        self.assertEquals(os.path.exists(filename), True)
        os.remove(filename)

    def test_to_csv_writes_file_path_column(self):
        filename = 'test_photos.csv'
        jph.PhotosList(PhotosListTest.photos).to_csv(filename)

        self.assertEquals


class JphScrapTest(unittest.TestCase):

    def test_produces_users_csv(self):
        pass

    def test_produces_albums_csv(self):
        pass

    def test_produces_photos_csv(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
