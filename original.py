import os
import requests
import pymysql as pp
from cachetools import cached, LRUCache, TTLCache
import tkinter as t
import datetime
window = t.Tk()
window.title("Google Books")
window.geometry('900x900')
window.configure(background = "white")

gbn=t.Entry(window,width=40)
gbn.pack()
db = pp.connect("localhost","root","Bits@2506","assig" )
cursor = db.cursor()

ans=t.Text(window,height=100,width=80)
cc=[]
class MyCache(LRUCache):
    def popitem(self):
        key,value=super().popitem()
        return key,value
#declaring cache memory of size 50
cache=MyCache(maxsize=50)

class gbooks():
    googleapikey="AIzaSyCLrT2XE-CYEzOmQeE0pCRKxwq9X2DBQmg"
    #displays all results given by the api on search page and creates necessary gui interfaces
    def search(self,value):
        start_time=datetime.datetime.utcnow()
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
        title=[]
        des=[]
        auth=[]
        
        for i in vinfo:
            for j in i:
                if j=='title':
                    title.append(i[j])
                elif j=='authors':
                    auth.append(i[j])
                elif j=='description':
                    des.append(i[j])
        end_time=datetime.datetime.utcnow()
        delta=(end_time-start_time)
        l=len(title)
        #creates buttons for different book titles
        for i in range(0,l):
            bt=t.Button(window,text=title[i],command= lambda i=i:gbooks().display(i,title,auth,des,delta.total_seconds()))
            cc.append(bt)
            bt.pack(expand=1)

    def search_isbn(self,value):
        start_time=datetime.datetime.utcnow()
        parms = {"q":value,'key':self.googleapikey}
        url="https://www.googleapis.com/books/v1/volumes?q=isbn:"+value
        r = requests.get(url)
        print (r.url)
        rj = r.json()
        print(rj)
        top=rj['items']
        vinfo=[]
        for i in top:
            for j in i:
                if(j=='volumeInfo'):
                    vinfo.append(i[j])
        title=[]
        des=[]
        auth=[]
        
        for i in vinfo:
            for j in i:
                if j=='title':
                    title.append(i[j])
                elif j=='authors':
                    auth.append(i[j])
                elif j=='description':
                    des.append(i[j])
        end_time=datetime.datetime.utcnow()
        delta=(end_time-start_time)
        l=len(title)
        #creates buttons for different book titles
        for i in range(0,l):
            bt=t.Button(window,text=title[i],command= lambda i=i:gbooks().display(i,title,auth,des,delta.total_seconds()))
            cc.append(bt)
            bt.pack(expand=1)

    #displays all the book details in a different gui page.Loads data from cache if available or else from api.
    def display(self,n,title,auth,des,dell):
        global cache
        root=t.Tk()
        root.title(title[n])
        root.geometry('900x900')
        root.configure(background = "white")
        to=""
        if(len(cache)>0 and title[n] in cache):
            start_time=datetime.datetime.utcnow()
            print("Displayed from cache : ",end='')
            to=cache[title[n]]
            end_time=datetime.datetime.utcnow()
            delta=end_time-start_time
            print(delta.total_seconds()," Seconds")
        else:
            start_time=datetime.datetime.utcnow()
            print("Displayed from API : ",end='')
            to="Book : "+title[n]+"\n\n"
            au=""
            for i in auth[n]:
                au+=" "+i+','
            to+="Authors : "+au+"\n\n"
            to+="Description : "+des[n]
            cache[title[n]]=to
            end_time=datetime.datetime.utcnow()
            delta=end_time-start_time
            print(delta.total_seconds()+dell," Seconds")
        sql="insert into history values('"+title[n]+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
        
        S = t.Scrollbar(root)
        T = t.Text(root, height=4, width=200)
        S.pack(side='right', fill='y')
        T.pack(side='left', fill='y')
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        T.insert(t.END,to)
        root.mainloop()
        
#Searches for the data in search bar
def search_my_book():
    search=gbn.get()
    dt_start=datetime.datetime.utcnow()
    for i in cc:
        i.pack_forget()
    if len(search) == 10 and search.isdigit():
        bk=gbooks()
        bk.search_isbn(search)
    else:
        bk=gbooks()
        bk.search(search)

def check_history():
    root=t.Tk()
    root.title("History")
    root.geometry('900x900')
    root.configure(background = "white")
    tt=t.Text(root,height=4,width=200)
    tt.pack(side='left',fill='y')
    sql="select * from history;"
    try:
        cursor.execute(sql)
        ress=cursor.fetchall()
        for j in ress:
            name=j[0]
            tt.insert(t.END,name)
            tt.insert(t.END,'\n')
    except:
        print("Error")
    

bt1=t.Button(window,text="Search Book",command=search_my_book)
bt1.pack()
bt2=t.Button(window,text=" Show History",command=check_history)
bt2.pack()
window.mainloop()
db.close()


