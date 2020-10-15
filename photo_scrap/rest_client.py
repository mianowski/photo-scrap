import os
import requests
import shutil
from pathlib import Path


def download_photo(url: str, local_path: str) -> bool:
    result = False
    try:
        r = requests.get(url, stream=True)
        if 200 == r.status_code:
            Path(os.path.dirname(local_path)).mkdir(
                parents=True, exist_ok=True)
            with open(local_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        result = (200 == r.status_code)
    except ConnectionError as e:
        print("Unable to download photo from: {}".format(url))
        print(e.strerror())
        result = False
    return result


class RestClient():
    API_URL = 'https://jsonplaceholder.typicode.com'

    @classmethod
    def get_user(cls, userId: int) -> dict:
        ret = requests.get(
            '/'.join((cls.API_URL, 'users', str(userId)))).json()
        return ret

    @classmethod
    def get_user_albums(cls, userId: int) -> dict:
        return requests.get('/'.join((cls.API_URL, 'users', str(userId), 'albums'))).json()

    @classmethod
    def get_album_photos(cls, album_id: int) -> dict:
        return requests.get('/'.join((cls.API_URL, 'albums', str(album_id), 'photos'))).json()
