from twitterdash.models import TwitterPage, TwitterPublicStat
from TwitterAPI import TwitterAPI
import regex
import time
import os
import datetime

class PageUpdater:

    def __init__(self):
        
        #read the keys, later this will be from a db

        keyfile = open('twitterdash/corefunctions/keys.txt','r')
        self.keys = []
        self.keynumber = 0
        for line in keyfile:
            line = regex.sub("\n|\r","",line).split(",")
            self.keys.append(line)
        
        keyfile.close()
        #send over the keys to be set

        self.setkey(self.keys[self.keynumber])
        
    def setkey(self,key):
        print "new key set"
        self.api = TwitterAPI(key[0],key[1],key[2],key[3])
    

    def load_pages(self,username):

        username = regex.sub("\r|\n","",username)
        result = self.api.request('users/show', {'screen_name':username})

        #if the quota is nearing end return
        if result.get_rest_quota()['remaining'] < 2 and result.get_rest_quota()['remaining'] != None:
            del self.api
            self.keynumber += 1
            self.setkey(self.keys[self.keynumber])
            result = self.api.request('users/show', {'screen_name':username})


        
        for user in result.get_iterator():

            try:
                new_page = TwitterPage(
                                        pageid = user['id'],
                                        username = user['screen_name'],
                                        name = user['name'],
                                        #language = user['status']['lang'],
                                        )
                new_page.save()
            except:
                print username + ": Failed " + str(self.keynumber)


    def update_followers(self,username):
        result = self.api.request('users/show', {'screen_name':username})

        #if the quota is nearing end return
        if result.get_rest_quota()['remaining'] < 2 and result.get_rest_quota()['remaining'] != None:
            del self.api
            self.keynumber += 1
            self.setkey(self.keys[self.keynumber])
            result = self.api.request('users/show', {'screen_name':username})

        twitterpage = TwitterPage.objects.get(username=username)

        for page in result.get_iterator():
            try:
                followers = page['followers_count']
                following = page['friends_count']
                favorites = page['favourites_count']
                status = page['statuses_count']
            except:
                followers = None
                following = None
                favorites = None
                status = None
                
            page_update = TwitterPublicStat(twitterpage = twitterpage,
                                            datepageid = str(datetime.date.today())+str(twitterpage.pageid),
                                            followers = followers,
                                            following = following,
                                            favorites = favorites,
                                            status = status,
                                            date = str(datetime.date.today()))
            page_update.save()
                                        
                                        
        


