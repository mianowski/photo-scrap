import requests
from urllib.parse import urlunparse

API_URL = 'https://jsonplaceholder.typicode.com'
class JphScrapper():
    def __init__(self, userIds:list=[], threads: int=1):
        self.userIds = userIds
        self.threads = threads
        
    def getUser(self, userId):
        return requests.get('/'.join((API_URL, 'users', str(userId)))).json()
    def getUserAlbums(self, userId):
        return requests.get('/'.join((API_URL, 'users', str(userId), 'albums'))).json()


if __name__=="__main__":
    scrap = JphScrapper()
    print(scrap.getUserAlbums(3))
