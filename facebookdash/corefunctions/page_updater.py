#import the database models
from facebookdash.models import FacebookPage, FacebookPost, FacebookPublicStat
#import other functions
import urllib
import json
import time
import sys
import datetime
from django.utils.timezone import utc

def load_page(pageid):
	url = "https://graph.facebook.com/" + pageid 
        try:
                response = urllib.urlopen(url)
                main_dic = json.load(response)
                new_page = FacebookPage(pageid = pageid,
                                        username = main_dic['username'],
                                        name = main_dic['name'],
                                        link = main_dic['link']
                                        )
                new_page.save()
        except:
                print "this page does not exist"
                return
	

	
def update_likes_ptat(pageid):

	#update the likes and ptat
	url = "https://graph.facebook.com/" + str(pageid)
	response = urllib.urlopen(url)
	main_dic = json.load(response)	
		
	#page ids
	facebookpage = FacebookPage.objects.get(pageid=pageid)
	
	#page likes
	update_stats = FacebookPublicStat(datepageid = str(datetime.date.today())+str(pageid),
                                        facebookpage=facebookpage,
					date = datetime.date.today().replace(tzinfo=utc),
					followers = main_dic['likes'],
                                        ptats = main_dic['talking_about_count'])
	update_stats.save()
