from django.db import models
from urldash.models import Url
# Create your models here.
class TwitterPage(models.Model):
	#this model stores the handels
	#on api: id
	pageid = models.BigIntegerField(primary_key = True)
	#on api: screen_name
	username = models.CharField(max_length=50,blank=True, null=True)
	#on api: name
	name = models.CharField(max_length=50,blank=True, null=True)
	#interface language
	language = models.CharField(max_length=50,blank=True, null=True)
	department = models.CharField(max_length = 40, blank=True, null=True)
	bureau = models.CharField(max_length = 40, blank=True, null=True)
	country = models.CharField(max_length = 50, blank=True, null=True)
	city = models.CharField(max_length = 50, blank=True, null=True)
	mission = models.CharField(max_length = 50, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.name)

class TwitterPublicStat(models.Model):
	#the datepageid attribute will be used for creating a unique key for each day
	#this way if the db is updated we won't have multiple entries a day
	datepageid = models.CharField(max_length=100, primary_key = True)
	date = models.DateField()
	followers = models.IntegerField()
	following = models.IntegerField()
	favorites = models.IntegerField()
	status = models.IntegerField() #user_statuses
	
	#many to one
	twitterpage = models.ForeignKey(TwitterPage)
	
	def __unicode__(self):
		return u'%s %s %s' % (self.twitterpage, self.date, self.followers)

class TwitterTweet(models.Model):
	#this model will store all of the tweets
	tweetid = models.BigIntegerField(primary_key=True)
	language = models.CharField(max_length=50, null=True)
	created_time = models.DateTimeField()
	message = models.TextField()
	retweets = models.IntegerField() #retweet_count
	favorites = models.IntegerField() # favorite_count
	in_reply_to_screen_name = models.CharField(max_length=50,null=True) #in_reply_to_screen_name
	media_type = models.CharField(max_length=20, null=True)
	media_url = models.URLField(null=True)
	retweeted_from = models.CharField(max_length=20,blank=True, null=True)

	#many to one
	twitterpage = models.ForeignKey(TwitterPage)
	#many to many but text for now
	urls = models.ManyToManyField(Url,blank=True)

	def __unicode__(self):
		message = self.message
                if message == None:
                        message = "NA"
		
		elif len(message) > 40:
			message = message[:40]

		return u'%s' % (message)


	def fuzzy_serach(self,strsearch ,*args, **kwds):
                #implements a fuzzy search
                from fuzzywuzzy.fuzz import ratio
                message = self.message

                if abs(len(message)-len(strsearch)) > len(message)*0.5:
                        return False
                else:
                        if ratio(message,strsearch) > 60:
                                return True
                        else:
                                return False
                



	
