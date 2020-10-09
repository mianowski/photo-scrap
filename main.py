from photo_scrap.jsonplaceholder import JphScrapper, PhotosList
import os
import threading
import json

if __name__ == '__main__':
    config = {'threads': 1,
              'photos_dir': os.path.join('..', 'photos'),
              'csv_dir': os.path.join('..', 'csv'),
              }
    try:
        with open(sys.argv[1]) as config_file:

            user_config = json.load(config_file)
            config.update(user_config)
    except:
        print("Cannot use config file, I'll load defaults")

    threads_count = config['threads']
    scrap = JphScrapper()
    user_ids = [1]
    users = scrap.get_users_list(user_ids)
    users.to_csv(os.path.join(config['csv_dir'], 'users.csv'))

    albums = scrap.get_user_albums(user_ids)
    albums.to_csv(os.path.join(config['csv_dir'], 'albums.csv'))
    photos = scrap.get_album_photos(albums.get_album_ids())
    photos_dir = config['photos_dir']
    photos.add_file_path_each_photo(photos_dir)
    photos.to_csv(os.path.join(config['csv_dir'], 'photos.csv'))
    split_photos = photos.split(threads_count)
    threads = []
    print('Downloading photos by {} threads'.format(threads_count))
    for elem in split_photos:
        thread = threading.Thread(target=elem.download_photos)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print('Downolading finished')
