#import the database models
from facebookdash.models import FacebookPage, FacebookPost, FacebookPublicStat
#import other functions
import urllib
import json
import time
import sys
import datetime
from django.utils.timezone import utc

#fill with karges
def load_page(line):

        line = line.replace('"','')
        line = line.split("\t")
        pageid = line[0]        
        
	url = "https://graph.facebook.com/" + pageid
	
        response = urllib.urlopen(url)
        main_dic = json.load(response)

        if "error" in main_dic.keys():
                return

        fields = {}
        try:
                fields['city'] = line[3]
                fields['country'] = line[5]
                fields['bureau'] = line[6]
                fields['mission'] = line[7]
                
        except:
                pass

        try:
                fields['username'] = main_dic['username']
        except:
                fields['username'] = "None"


        new_page = FacebookPage(pageid = pageid,
                                name = main_dic['name'],
                                link = main_dic['link'],
                                **fields
                                )
        new_page.save()
   

	
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
					date = datetime.date.today(),
					followers = main_dic['likes'],
                                        ptats = main_dic['talking_about_count'])
	update_stats.save()
