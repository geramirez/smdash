from twitterdash.models import TwitterPage, TwitterTweet
from urldash.models import Url
from TwitterAPI import TwitterAPI
from time import sleep, time
import regex
import datetime
from django.utils.timezone import utc
import urllib
from photohash import average_hash

class TweetGetter:

    def __init__(self):

        #read the keys, later this will be from a db
        keyfile = open('twitterdash/corefunctions/keys.txt','r')
        self.keys = []
        self.keynumber = 0
        for line in keyfile:
            line = regex.sub("\n|\r","",line).split(",")
            self.keys.append(line)

        keyfile.close()

        #set up the call dictionary
        self.calldic =  { 'count':'100',
                          'exclude_replies':'false',
                          'include_rts':'true'}

        #send over the keys to be set
        self.setkey(self.keys[self.keynumber])

        #create the last date
        self.lastday = datetime.datetime.fromtimestamp(int(time()) - 604800/2)

    def setkey(self,key):

        self.api = TwitterAPI(key[0],key[1],key[2],key[3])

    def gettweets(self,username):

        #get the twitter page
        self.twitterpage = TwitterPage.objects.get(username=username)
        #add the user name to dict
        self.calldic['screen_name'] = regex.sub("\r|\n","",username)

        keepgoing = True
        while keepgoing:
            #make call
            self.make_api_call()

            #check if last date collected is greater than last date
            if  self.last_time_in_list > self.lastday:
                self.calldic['max_id'] = str(self.last_tweet_id_in_list - 1)
            else:
                keepgoing = False
                #del the max id
                if self.calldic.has_key('max_id'):
                    del self.calldic['max_id']

      
    def make_api_call(self):

        result = self.api.request('statuses/user_timeline', self.calldic)
        print result.get_rest_quota()['remaining'],  self.calldic['screen_name']
        #if the quota is nearing end move to new key
        if result.get_rest_quota()['remaining'] < 2 and result.get_rest_quota()['remaining'] != None:
            del self.api
            sleep(200)
            self.keynumber += 1
            self.keynumber = self.keynumber % 2
            self.setkey(self.keys[self.keynumber])
       
        for tweet in result.get_iterator():
            #exit if error
            try:
                tweetid = tweet['id']
            except:
                print "No more calls left"
                return "shit"

            language = tweet['lang']
            #get date

            created_time = datetime.datetime.strptime(tweet['created_at'].encode('utf-8'),"%a %b %d %H:%M:%S +0000 %Y")
            #fix date
            time = created_time.replace(tzinfo=utc)
            
            message = tweet['text'].encode('utf-8')
            retweets = tweet['retweet_count']
            favorites = tweet['favorite_count']
            in_reply_to_screen_name = tweet['in_reply_to_screen_name']
            
            #these should be tested
            if tweet['entities'].has_key('media'):
                media_type = tweet['entities']['media'][0]['type']
                urllib.urlretrieve(tweet['entities']['media'][0]['media_url'].encode('utf-8'),"temp_pic.jpg")
                picture = average_hash("temp_pic.jpg", hash_size = 64)
                
            else:      
                media_type = None
                picture = None

            if tweet.has_key('retweeted_status'):
                retweeted_from = tweet['retweeted_status']['user']['screen_name'].encode('utf-8')
            else:
                retweeted_from = None
                
            if tweet['entities'].has_key("urls"):
                for url in tweet['entities']['urls']:
                    message = regex.sub(url['url'].encode('utf-8'),url['expanded_url'].encode('utf-8'),message)
           
            
            tweet_update = TwitterTweet(tweetid = tweetid,
                                         language = language,
                                         created_time = time,
                                         message = message,
                                         retweets = retweets,
                                         favorites = favorites,
                                         in_reply_to_screen_name = in_reply_to_screen_name,
                                         media_type = media_type,
                                         picture = picture,
                                         retweeted_from = retweeted_from,
                                         twitterpage = self.twitterpage,
                                        )

            tweet_update.save()

            #add urls
            
            if tweet['entities'].has_key("urls"):
                for url in tweet['entities']['urls']:
                    try:
                        new_url = Url(url = url[u'expanded_url'].encode('utf-8'))
                        new_url.save()
                        tweet_update.urls.add(new_url)
                    except:
                        pass

            
        #try to get the created time
        try:
            self.last_time_in_list = created_time
            self.last_tweet_id_in_list = tweetid
        #if not feed it a break
        except:
            "no tweets"
            self.last_time_in_list = datetime.datetime(1900,1,1)
