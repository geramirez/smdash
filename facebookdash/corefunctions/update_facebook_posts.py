from facebookdash.models import FacebookPage,FacebookPost
from django.shortcuts import render
from django.http import HttpResponse
from facebookdash.corefunctions import post_updater

def update(request):
	#upate the page posts for each page
	if 'pwd' in request.GET and 'update' == request.GET['pwd']:

                f = open("facebookdash\corefunctions\key.txt")
		key = f.read()
		f.close()
		print key
		for page in FacebookPage.objects.all():
			instance = post_updater.FPA(key)
			instance.getposts(page.pageid)
		
		return render(request, 'update_facebook_posts.html',{'done':True})
	
	else:
		return render(request, 'update_facebook_posts.html')
