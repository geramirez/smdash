from django.db import models
from urldash.models import Url

class FacebookPage(models.Model):
	#on api: id
	pageid = models.BigIntegerField(primary_key = True)
        #on api: username
	username = models.CharField(max_length=40, blank=True, null=True)
        #on api: name
	name = models.CharField(max_length=100,blank=True, null=True)
	link = models.URLField(blank=True, null=True)
	department = models.CharField(max_length = 40, blank=True, null=True)
	bureau = models.CharField(max_length = 40, blank=True, null=True)
	country = models.CharField(max_length = 50, blank=True, null=True)
	city = models.CharField(max_length = 50, blank=True, null=True)
	mission = models.CharField(max_length = 50, blank=True, null=True)
	
	def __unicode__(self):
		return u'%s' % (self.name)
	
       
class FacebookPost(models.Model):
	
	postid = models.CharField(max_length=40,primary_key = True)
	message = models.TextField(null=True)
	kind = models.CharField(max_length=8)
	created_time = models.DateTimeField()
	likes = models.IntegerField()
	shares = models.IntegerField()
	comments = models.IntegerField()
	picture = models.URLField(null=True)

	#Many to one
	facebookpage = models.ForeignKey(FacebookPage)
	
	#many to many but text for now
	urls = models.ManyToManyField(Url,blank=True)
	
	def __unicode__(self):
		message = self.message
                if message == None:
                        message = "NA"
		
		elif len(message) > 40:
			message = message[:40]

		return u'%s %s' % (message, self.kind)

	def fuzzy_serach(self,strsearch ,*args, **kwds):
                #implements a fuzzy search
                from fuzzywuzzy.fuzz import ratio
                message = self.message

                if message == None:
                        return False

                if abs(len(message)-len(strsearch)) > len(message)*0.5:
                        return False
                else:
                        if ratio(message,strsearch) > 65:
                                return True
                        else:
                                return False
                
	
	class Meta:
		ordering = ['created_time']
		
class FacebookPublicStat(models.Model):
	#the datapageid attribute will be used for creating a unique key for each day
	#this way if the db is updated we won't have multiple entries a day
	datepageid = models.CharField(max_length=100,primary_key = True)	
	followers = models.IntegerField()
	ptats = models.IntegerField()
	date = models.DateField()	
	
	#Many to one
	facebookpage = models.ForeignKey(FacebookPage)

	def __unicode__(self):
		return u'%s %s %s' % (self.page, self.date, self.likes, self.ptats)
	

