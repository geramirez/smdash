import mailchimp
from mailchimpdash.models import *
from twitterdash.models import *
import urllib
#TODO Get the fuzzysaerch imported
def updateEmails():
    #Open API
    api = mailchimp.Mailchimp("f2b3b466024304b6cdc43b26e9b32194-us8")
    allcampaigns=api.campaigns.list()
    campaignids={}
    #Get a list of all campaignids
    for item in allcampaigns['data']:
        if item['status']=='sent':
           campaignids[item['id']]=item['title']
           
    #make appropriate api calls for each item saved
    for item in campaignids.keys():
        summ=api.reports.summary(cid=item)
        clicked=summ['clicks']
        opened=summ['opens']
        Dated=summ['timeseries'][0]['timestamp']
        Dates=Dated[0:10]
        cont=api.campaigns.content(cid=item)
        html=cont['html']
        text=cont['text']
        cid=item
        name=campaignids[item]
        #Create object
        E=Email(Campaign_id=cid,
                Campaign_name=name,
                  Date=Dates,
                  Email_html=html,
                  Email_text=text,
                  clicks=clicked,
                  opens=opened
                  )
        #Save object
        E.save()

def updateTweets():
    #GET ALL EMAILS
    emails=Email.objects.all()
    for msg in emails:
        Tweets=ExtractTweets(msg.Email_text)
        print Tweets
        for item in Tweets:
            Tweetmatches=fuzzsearch(item.decode('utf-8','ignore'), msg.Date, msg.Date.replace(day=(msg.Date.day+3)))
            print "Fuzz search done", len(Tweetmatches),'matches found'
            for i in Tweetmatches:
                print "HEEY"
                t=EmailTweets(idnum=(str(i.tweetid)+str(msg.Campaign_id)+str(item[0:20])), Campaign_id=msg, Tweet=item,
                        TweetMatch=i)
                t.save()
                
def ExtractTweets(text):
  Tweets=[]
  line=''
  for char in text:
    line=line+char
    if char=='\n':
        if 'http://twitter.com/intent/tweet?text=' in line:
           b= urllib.unquote(line[37:].encode('utf-8'))
           tweet=''
           for char in b:
                tweet=tweet+char
                if 'Tweet' in tweet:
                    tweet=tweet[:-5]
                    Tweets.append(tweet)
                    break
        line=''
  return Tweets



def fuzzsearch(q,d1,d2):

	    twittertweets = TwitterTweet.objects.filter(created_time__range=[d1,d2])
            print "APPLE"
	    twittertweets = [post for post in twittertweets if post.fuzzy_serach(q)]
        
            return twittertweets


