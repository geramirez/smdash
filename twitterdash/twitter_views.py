from django.shortcuts import render
from django.http import HttpResponse
from twitterdash.models import TwitterTweet
from django.db.models import Q
import datetime
import HTMLParser

def search_form(request):
    return render(request, 'search_twitter_form.html')
	
def search(request):
    errors = []
    if 'q' in request.GET:
		q = request.GET['q']
        
		if not q:
			errors.append('Enter a search term.')
		elif len(q) > 20:
			errors.append('Please enter at most 20 characters.')	
		else:
                        #get the dates
                        enddate = datetime.date.today()
                        startdate = enddate - datetime.timedelta(days=7)
                        #make the query
			posts = TwitterTweet.objects.filter(created_time__range=[startdate, enddate])\
                                .filter(Q(message__iregex=q))\
                                .filter(retweeted_from__isnull=True)\
                                .extra(select = {'fieldsum':'retweets + favorites'}, order_by = ('-fieldsum',))
                        
			return render(request, 'search_twitter_results.html',
					{'posts': posts, 'query': q})
		
    return render(request, 'search_twitter_form.html',
        {'error': errors})

def topten_tweets(request):
    #gets the top 10 and formats them

    #get the dates
    enddate = datetime.date.today()
    startdate = enddate - datetime.timedelta(days=7)

    #make query
    tweets = TwitterTweet.objects.filter(created_time__range=[startdate, enddate])\
                                .filter(retweeted_from__isnull=True)\
                                .extra(select = {'fieldsum':'retweets + favorites'}, order_by = ('-fieldsum',))[0:10]

    TweetsHTML = []

    for tweet in tweets:
        TweetsHTML.append(convertTweetToHtml(tweet))
       
    return render(request, 'top_10_tweets.html',
                  {'tweets':TweetsHTML})


def convertTweetToHtml(tweet):
    
    tweetdict = {'username':tweet.twitterpage.username,
                 'name':tweet.twitterpage.name,
                 'message':tweet.message,
                 'tweetid':str(tweet.tweetid),
                 'created_time':str(tweet.created_time),
                 'ftime':str(tweet.created_time)}

    html_parser = HTMLParser.HTMLParser()
        
    htmlTweet = """<blockquote class="twitter-tweet tw-align-center" width="350"><p>%(message)s</p>&mdash; %(name)s (%(username)s) <a href="https://twitter.com/%(username)s/status/%(tweetid)s" data-datetime="%(created_time)s">%(ftime)s</a></blockquote><script src="http://platform.twitter.com/widgets.js" charset="utf-8"></script>""" 
    htmlTweet = htmlTweet % tweetdict
    return html_parser.unescape(htmlTweet)
