from django.db import models

# Create your models here.
class Email(models.Model):
    Campaign_id=models.CharField(max_length=30, primary_key=True)
    Campaign_name=models.CharField(max_length=60)
    Date=models.DateField()
    Email_html=models.CharField(max_length=5000000)
    Email_text=models.CharField(max_length=5000000)
    clicks=models.IntegerField()
    opens=models.IntegerField()

class EmailTweets(models.Model):
    idnum=models.CharField(max_length=100, primary_key=True)
    Campaign_id=models.ForeignKey(Email)
    Tweet=models.CharField(max_length=300)
    TweetMatch=models.ForeignKey('twitterdash.TwitterTweet')
    ordering=['Campaign_id.Date']

class EmailFacebookPosts(models.Model):
    idnum=models.CharField(max_length=50, primary_key=True)
    Campaign_id=models.ForeignKey(Email)
    FacebookPost=models.CharField(max_length=3000)
    FacebookPostMatch=models.ForeignKey('facebookdash.FacebookPost')

class EmailPictures(models.Model):
    idnum=models.CharField(max_length=50, primary_key=True)
    Campaign_id=models.ForeignKey(Email)
    Image=models.CharField(max_length=70)
    ImgURL=models.CharField(max_length=500)
    ImgMatch=models.ForeignKey('facebookdash.FacebookPost')

#I DONT LIKE THE EMAIL PICTURES MODEL

class EmailLinks(models.Model):
    idnum=models.CharField(max_length=50, primary_key=True)
    Campaign_id=models.ForeignKey(Email)
    link=models.CharField(max_length=500)
    ImgMatch=models.ForeignKey('facebookdash.FacebookPost')
"""    
class TweetMatches(models.Model):
    Tweet_id=models.ForeignKey('EmailTweets', to_field='Tweet_id') #Many to Many
    TwitterPost=models.ForeignKey('twitterdash.TwitterTweet')
    
class FBMatches(models.Model):
    FacebookPost_id=models.ForeignKey('EmailFacebookPosts',to_field='FacebookPost_id')
    FacebookPost=models.ForeignKey('facebookdash.FacebookPost')
"""
