from photo_scrap.scrapper import PhotoScrapper
from photo_scrap.rest_client import RestClient
import os
import sys
import json


def main():
    config = {'threads': 8,
              'photos_dir': os.path.join('..', 'photos'),
              'csv_dir': os.path.join('..', 'csv'),
              'user_ids': [1]
              }

    try:
        with open(sys.argv[1]) as config_file:
            user_config = json.load(config_file)
            config.update(user_config)
    except Exception as e:
        print("Cannot use config file, I'll load defaults")
        print(e)

    threads_count = config['threads']
    user_ids = config['user_ids']
    csv_dir = config['csv_dir']
    photos_dir = config['photos_dir']

    scrapper = PhotoScrapper(RestClient())
    users_list = scrapper.get_users_list(user_ids, threads_count)
    users_list.to_csv(os.path.join(csv_dir, 'users.csv'))

    albums = scrapper.get_user_albums(user_ids, threads_count)
    albums.to_csv(os.path.join(csv_dir, 'albums.csv'))

    photos = scrapper.get_album_photos(
        albums.get_album_ids(), threads_count)
    photos.add_file_path_each_photo(photos_dir)
    photos.to_csv(os.path.join(csv_dir, 'photos.csv'))
    photos.download_photos(threads_count)


if __name__ == '__main__':
    main()
