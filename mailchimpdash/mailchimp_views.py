from django.shortcuts import render
from mailchimpdash.models import *
from corefunctions.mailchimp_update import *
from corefunctions.supplementalfunctions import *
# Create your views here.
from PIL import *


def UpdateMailchimp(request):
	#upate the page posts for each page
	if 'pwd' in request.GET and 'update' == request.GET['pwd']:

                updateEmails()
                print "DO"
	else:
		return render(request, 'updated.html')
	return render(request, 'updated.html',{'done':True})

def UpdateTweets(request):
        if 'pwd' in request.GET and 'update' == request.GET['pwd']:

                updateTweets()
                print "DO"
	else:
		return render(request, 'update2.html')
	return render(request, 'update2.html',{'done':True})

def MailchimpReport(request):


        E=EmailTweets.objects.all()
        #Get list of all emails
        #get independent lists of each of the items from each email
        #Get independent lists of each of the tweets
        #
                
        return render(request,'MailchimpReport.html',{'matches':E})

def UpdateImages(request):
        updateImages()

        return render(request,'done.html')
