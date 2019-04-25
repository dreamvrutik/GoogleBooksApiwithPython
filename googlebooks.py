from cachetools import cached, LRUCache, TTLCache
import os
import requests

class MyCache(LRUCache):
    def popitem(self):
        key,value=super().popitem()
        return key,value


class gbooks():
    googleapikey="AIzaSyCLrT2XE-CYEzOmQeE0pCRKxwq9X2DBQmg"

    def search(self, value):
        parms = {"q":value, 'key':self.googleapikey}
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        print (r.url)
        rj = r.json()
        top=rj['items']
        vinfo=[]
        for i in top:
            for j in i:
                if(j=='volumeInfo'):
                    vinfo.append(i[j])
        for i in vinfo:
            for j in i:
                print(j)
        

if __name__ == "__main__":
    bk = gbooks()
    cc=MyCache(maxsize=5)
    bk.search("harry")
    print(cc)
    if('William and Harry' in cc):
        print("hi")
