#import the database models
from facebookdash.models import FacebookPage,FacebookPost
from urldash.models import Url
#import other functions
import urllib2
import urllib
import json
import time
import sys
import regex
import datetime
from django.utils.timezone import utc

class FPA:

	def __init__(self,token):
		
	    #initializes the class and sets up the tokens
		self.token = token
		#set up the current time
		
		self.date = time.time()
		self.firstday = str(int(time.time()))
		self.lastday = str(int(self.date - 604800 * 2))
		
		#set limit
		self.limit = '100'
		
	def getposts(self,pageid):
		#initialize the page to be updated
		facebookpage = FacebookPage.objects.get(pageid=pageid)
		#print "FB " + facebookpage.username
		#define the page and parameters
		url = "https://graph.facebook.com/v2.0/" + regex.sub("\r|\n| ","",str(pageid)) + "/posts?"
		
		headers =  urllib.urlencode({
			'limit':self.limit,
			'until':self.firstday,
			'date_format':'U',
			'fields':'message,shares,link,id,from,picture,type,likes.summary(true).limit(1),comments.summary(true).limit(1)',
			'access_token':self.token
			})
		#get the first update
		main_dic = self.open_page(url + headers)
		
		#start a loop for paging
		keep_going = True
		while keep_going == True:

			#check if data is empty
			if main_dic == None or main_dic['data'] == []:
                                print "something is very wrong"
				return
			
                    #extract posts if not empty
			for post in main_dic['data']:
				
				#get created time, stop if its out of range
				created_time = post['created_time']
				if int(self.lastday) > created_time:
					return

				time = datetime.datetime.fromtimestamp(created_time).replace(tzinfo=utc)

				created_time = str(created_time)
                
				#get the post id
				postid = post['id'].encode('utf-8')
				
                                #get the type of post
				kind = post['type'].encode('utf-8')
                
                                #get the message
				if "message" in post.keys():
					message = post['message'].encode('utf-8')
				else:
					message = None

				#get picture
				if "picture" in post.keys():
					picture = post['picture'].encode('utf-8')
				else:
					picture = None
				
                                #get the number of shares
				if "shares" in post.keys():
					shares = post['shares']['count']
				else:
					shares = 0

				#get the likes
				if "likes" in post.keys():
					likes = post['likes']['summary']['total_count']
				else:
					likes = 0

                                #get the comments
				if "comments" in post.keys():
					comments = post['comments']['summary']['total_count']
				else:
					comments = 0

				if kind=="link" and "link" in post.keys():
                                        if message == None:
                                                message = ""
                                        message = message + " url:" + post['link'].encode('utf-8')
				
				#update data
				post_update = FacebookPost(postid = postid,
							message = message,
							kind = kind,
							created_time = time,
							likes = likes,
							shares = shares,
							comments = comments,
							picture = picture,
							facebookpage = facebookpage )
				post_update.save()



				#get link
				
				try:
                                        if kind=="link" and "link" in post.keys():
                                                link = post['link'].encode('utf-8')
                                                new_url = Url(url=link)
                                                new_url.save()
                                                post_update.urls.add(new_url)
                                except:
                                        print "already there?",new_url
					

				
            #determin to continue
			nextpage =  main_dic['paging']['next'].encode('utf-8')
			main_dic = self.open_page(nextpage)
		

	def open_page(self,url):
		try:
			response = urllib2.urlopen(url)
			main_dic = json.load(response)
			return main_dic
		except:
			print "failed"
			return None
