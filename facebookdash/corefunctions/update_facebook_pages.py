from facebookdash.models import FacebookPage, FacebookPost, FacebookPublicStat
from django.shortcuts import render
from django.http import HttpResponse
from facebookdash.corefunctions import page_updater

###this function loops through the pages in 
###a csv file and updates them into the page db

def load(request):
	if 'pwd' in request.GET and 'load' == request.GET['pwd']:

		#open the file and loop through
		f = open("facebookdash/corefunctions/DOSAccounts.txt","r")

		for pageid in f:
			page_updater.load_page(pageid)

		f.close()
		return render(request, 'load_facebook_pages.html',{'done':True})
		
	else:
		return render(request, 'load_facebook_pages.html')
		
		
def update_facebook_page_stats(request):
	if 'pwd' in request.GET and 'update' == request.GET['pwd']:
		
		for page in FacebookPage.objects.all():
			page_updater.update_likes_ptat(page.pageid)
		
		return render(request, 'update_facebook_page_stats.html',{'done':True})
		
	else:
		return render(request, 'update_facebook_page_stats.html')
