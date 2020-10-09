import os
import requests
import shutil
from pathlib import Path


class RestClient():
    API_URL = 'https://jsonplaceholder.typicode.com'

    @staticmethod
    def getUser(userId: int):
        return requests.get('/'.join((RestClient.API_URL, 'users', str(userId)))).json()

    @staticmethod
    def get_user_albums(userId: int):
        return requests.get('/'.join((RestClient.API_URL, 'users', str(userId), 'albums'))).json()

    @staticmethod
    def getAlbumPhotos(album_id: int):
        return requests.get('/'.join((RestClient.API_URL, 'albums', str(album_id), 'photos'))).json()

    @staticmethod
    def downloadPhoto(url: str, local_path: str):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            Path(os.path.dirname(local_path)).mkdir(
                parents=True, exist_ok=True)
            with open(local_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)


if __name__ == '__main__':
    RestClient.downloadPhoto(
        'https://via.placeholder.com/150/56a8c1asd', './test.png')
