from django.shortcuts import render
from main.forms import CampaignSearchForm,ContentSearchForm
from django.http import HttpResponseRedirect
from facebookdash.models import FacebookPost
from twitterdash.models import TwitterTweet
from django.db.models import Q, Sum, Count
import datetime
from django.utils.timezone import utc

def CampaignSearch(request):



    if request.method == "POST" and request.POST.has_key("keyword"):
        form = CampaignSearchForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            #set first day
            firstday = datetime.datetime.combine(cd['firstday'],datetime.time()).replace(tzinfo=utc)
            #set last day
            lastday = datetime.datetime.combine(cd['lastday'],datetime.time()).replace(tzinfo=utc)

            #query
            q = cd['keyword']
            
            #query the database
            facebookstats = FacebookPost.objects\
                                .filter(created_time__range=[firstday, lastday])\
                                .filter(Q(message__iregex=q))\
                                .aggregate(Sum('shares'),
                                           Sum('comments'),
                                           Sum('likes'),
                                           Count('postid'),
                                           Count('facebookpage',distinct=True))


            #twitter query

	    twitterstats = TwitterTweet.objects.filter(created_time__range=[firstday, lastday])\
                                .filter(Q(message__iregex=q))\
                                .aggregate(Sum('retweets',retweeted_from__isnull=True),
                                     Sum('favorites',retweeted_from__isnull=True),
                                     Count('tweetid',retweeted_from__isnull=True),
                                     Count('twitterpage',distinct=True),
                                     Count('retweeted_from'))

            return render(request, 'campaign_search_results.html',{'stats_page':'stats_page',
                                                                   'facebookstats':facebookstats,
                                                                   'twitterstats':twitterstats,
                                                                   'query': q,
                                                                   'firstday':firstday,
                                                                   'lastday':lastday})

    elif request.method == "POST" and request.POST.has_key("test"):
        return render(request,'campaign_search_results.html',{'form':form})

    else:
        #set defaults
        form = CampaignSearchForm(initial={u'lastday':datetime.date.today()})

        return render(request,'campaign_search.html',{'form':form})

def ContentSearch(request):

    if request.method == "POST" and request.POST.has_key("keyword"):
        form = ContentSearchForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            
            cd = form.cleaned_data
            #set first day
            firstday = datetime.datetime.combine(cd['firstday'],datetime.time()).replace(tzinfo=utc)
            #set last day
            lastday = datetime.datetime.combine(cd['lastday'],datetime.time()).replace(tzinfo=utc)

            #query
            q = cd['keyword']
            
            #query the database
            '''
            facebookstats = FacebookPost.objects\
                                .filter(created_time__range=[firstday, lastday])\
                                .filter(Q(message__iregex=q))\
                                .aggregate(Sum('shares'),
                                           Sum('comments'),
                                           Sum('likes'),
                                           Count('postid'),
                                           Count('facebookpage',distinct=True))
            '''
            facebookposts = FacebookPost.objects\
                                .filter(created_time__range=[firstday, lastday])

            facebookposts = [post for post in facebookposts if post.fuzzy_serach(q)]
            


            #twitter query
            '''
	    twitterstats = TwitterTweet.objects.filter(created_time__range=[firstday, lastday])\
                                .filter(Q(message__iregex=q))\
                                .aggregate(Sum('retweets',retweeted_from__isnull=True),
                                     Sum('favorites',retweeted_from__isnull=True),
                                     Count('tweetid',retweeted_from__isnull=True),
                                     Count('twitterpage',distinct=True),
                                     Count('retweeted_from'))
            '''
	    twittertweets = TwitterTweet.objects.filter(created_time__range=[firstday, lastday])

	    twittertweets = [post for post in twittertweets if post.fuzzy_serach(q)]

            return render(request, 'content_search_results.html',{'stats_page':'stats_page',
                                                                   'facebookposts':facebookposts,
                                                                   'twittertweets':twittertweets,
                                                                   'query': q,
                                                                   'firstday':firstday,
                                                                   'lastday':lastday})

    elif request.method == "POST" and request.POST.has_key("test"):
        return render(request,'content_search_results.html',{'form':form})

    else:
        #set defaults
        form = ContentSearchForm(initial={u'lastday':datetime.date.today()})

        return render(request,'content_search.html',{'form':form})
