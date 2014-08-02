from twitterdash.models import TwitterPage
from django.shortcuts import render
from twitterdash.corefunctions import page_updater

def load(request):
	#upate the page posts for each page
	if 'pwd' in request.GET and 'load' == request.GET['pwd']:
                #open file and read pages
                f = open("twitterdash/corefunctions/twitter_accounts.csv",'r')

                #set instance
                instance = page_updater.PageUpdater()
                
                for line in f:
                        instance.load_pages(line)
		
		
		return render(request, 'load_twitter_pages.html',{'done':True})
	
	else:
		return render(request, 'load_twitter_pages.html')

def update(request):
	#upate the page posts for each page
	if 'pwd' in request.GET and 'update' == request.GET['pwd']:

                #set instance
                instance = page_updater.PageUpdater()
                
		for page in TwitterPage.objects.all():
                        instance.update_followers(page.username)
		
		
		return render(request, 'update_twitter_pages.html',{'done':True})
	
	else:
		return render(request, 'update_twitter_pages.html')
