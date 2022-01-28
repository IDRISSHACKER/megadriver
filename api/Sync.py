from ast import Try
from urllib.request import Request
from mega import Mega
import sqlite3


class Sync:
    def __init__(self):
        super(Sync, self).__init__()
        self.mega = Mega()
        self.user = False
        

    def login(self, email="idrisscoder@gmail.com", password="Michel02282003"):
        try:
            self.user = self.mega.login(email, password)
            return True
        except:
            return False
        

    def getUserInfos(self):
        details = self.user.get_user()
        return details

    def internet_on():
        url = "http://www.kite.com"
        timeout = 5
        try:
            request = Request.get(url, timeout=timeout)
            return True
        except:
            return True

    def freeSpace(self):
        space = self.user.get_storage_space(giga=True)
        return space
    
    def uploadFile(self, filename):
        try:
            self.user.upload(filename)
            return  True
        except:
            return False
    
    def upload(self, destination):
        self.login()
        self.user.export((destination, None))

    def findFolder(self, folder):
        folder = self.user.find(folder)
        return folder
    
    def restoreFolder(self, folder, destination="C:/"):
        folder = self.findFolder(folder)
        self.user.download(folder, destination)