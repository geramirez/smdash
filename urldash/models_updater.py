from django.db import models
from urldash.models import Url
import urllib2
import re

print "help"
#find urls that haven't been updated
url_list = Url.objects.filter(shorttype__isnull=True)

for url in url_list:
        print url
        try:
                destination = urllib2.urlopen(url.url).geturl()
                print destination
        
                if destination == url.url:
                        url.is_short = False
                else:
                        url.is_short.add(True)
                        url.shorturl.add(url.url)
                        url.longurl.add(destination)
                        url.shorttype.add(re.findall("http://(.*)/",url.url)[0])
                        print url.shorttype
        except:
                print "faild", url.url
        
        url.save()
                
