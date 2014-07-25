from twitterdash.models import TwitterPage, TwitterTweet
from django.shortcuts import render
from twitterdash.corefunctions import tweet_updater

def update(request):
	#upate the page posts for each page
	if 'pwd' in request.GET and 'update' == request.GET['pwd']:

                #load module
                instance = tweet_updater.TweetGetter()
                
		for page in TwitterPage.objects.all():
                    instance.gettweets(page.username)
		
		return render(request, 'update_twitter_posts.html',{'done':True})
	
	else:
		return render(request, 'update_twitter_posts.html')
