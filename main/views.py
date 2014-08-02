from django.shortcuts import render
from main.forms import CampaignSearchForm , ContentSearchForm , TopTenFormFacebook,TopTenFormTwitter
from django.http import HttpResponseRedirect
from facebookdash.models import FacebookPost
from twitterdash.models import TwitterTweet
from django.db.models import Q, Sum, Count
import datetime
from django.utils.timezone import utc
import HTMLParser

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
            
            #facebook query
            facebookstats = FacebookPost.objects.summarize(q,[firstday,lastday])
            facebookposts = FacebookPost.objects.get_posts(q,[firstday,lastday])
            
            #twitter query
	    twitterstats = TwitterTweet.objects.summarize(q,[firstday,lastday])
	    twittertweets = TwitterTweet.objects.get_tweets(q,[firstday,lastday])

            return render(request, 'campaign_search_results.html',{'stats_page':'stats_page',
                                                                   'facebookstats':facebookstats,
                                                                   'twitterstats':twitterstats,
                                                                   'facebookposts':facebookposts,
                                                                   'twittertweets':twittertweets,
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

            facebookposts = FacebookPost.objects\
                                .filter(created_time__range=[firstday, lastday])

            facebookposts = [post for post in facebookposts if post.fuzzy_serach(q)]
            


            #twitter query

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

def TopTenFacebook(request):
    
    if request.method == "POST":
        form = TopTenFormFacebook(request.POST)
        if form.is_valid():
            
            cd = form.cleaned_data
            returndict = {}
            #set first day
            firstday = datetime.datetime.combine(cd['firstday'],datetime.time()).replace(tzinfo=utc)
            #set last day
            lastday = datetime.datetime.combine(cd['lastday'],datetime.time()).replace(tzinfo=utc)
            #add date to return dict
            returndict['firstday'] = firstday
            returndict['lastday'] = lastday

            kwargs = {'created_time__range':[firstday, lastday]}
                
                #if there are twitter pages only get them 
            if bool(cd['facebookpageids']):
                kwargs['facebookpage__in']=cd['facebookpageids']
                
            if bool(cd['keyword']):
                kwargs['message__iregex']=cd['keyword']
            '''

            if bool(cd['countryids']):
                kwargs['facebookpage__country__in']=cd['countryids']

            if bool(cd['regionids']):
                kwargs['facebookpage__bureau__in']=cd['regionids']

            if bool(cd['cityids']):
                kwargs['facebookpage__city__in']=cd['cityids']
            '''

            posts = FacebookPost.objects.filter(**kwargs)\
                                    .extra(select = {'fieldsum':'shares + likes + comments'}, order_by = ('-fieldsum',))[0:10]

            PostsHTML = []
            for post in posts:
                PostsHTML.append(convertPostToHtml(post))

            returndict['posts'] = PostsHTML


            return render(request,'top_ten_results.html',returndict)

    form = TopTenFormFacebook(initial={u'lastday':datetime.date.today()})
    return render(request,'top_ten_search.html',{'form':form})


def TopTenTwitter(request):
    
    if request.method == "POST":
        form = TopTenFormTwitter(request.POST)

        if form.is_valid():
            returndict = {}
            cd = form.cleaned_data
            print cd
            #set first day
            firstday = datetime.datetime.combine(cd['firstday'],datetime.time()).replace(tzinfo=utc)
            #set last day
            lastday = datetime.datetime.combine(cd['lastday'],datetime.time()).replace(tzinfo=utc)
            #add date to return dict
            returndict['firstday'] = firstday
            returndict['lastday'] = lastday

            #set kwargs
            kwargs = {'created_time__range':[firstday, lastday],'retweeted_from__isnull':True}
                
                #if there are twitter pages only get them 
            if bool(cd['twitterpageids']):
                kwargs['twitterpage__in']=cd['twitterpageids']
                    
            if bool(cd['keyword']):
                kwargs['message__iregex']=cd['keyword']
            '''
            if bool(cd['countryids']):
                kwargs['twitterpage__country__in']=cd['countryids']

            if bool(cd['regionids']):
                kwargs['twitterpage__bureau__in']=cd['regionids']

            if bool(cd['cityids']):
                kwargs['twitterpage__city__in']=cd['cityids']
            '''

                
            tweets = TwitterTweet.objects.filter(**kwargs)\
                                    .extra(select = {'fieldsum':'retweets + favorites'}, order_by = ('-fieldsum',))[0:10]

            TweetsHTML = []
            for tweet in tweets:
                TweetsHTML.append(convertTweetToHtml(tweet))

            returndict['tweets'] = TweetsHTML
            

            return render(request,'top_ten_results.html',returndict)


    form = TopTenFormTwitter(initial={u'lastday':datetime.date.today()})
    return render(request,'top_ten_search.html',{'form':form})

    

def convertPostToHtml(post):
    postdic = {"username":post.facebookpage.username,
               "postid":post.postid.split("_")[1]}

    html_parser = HTMLParser.HTMLParser()
        
    htmlPost = """<div class="fb-post" data-href="https://www.facebook.com/%(username)s/posts/%(postid)s" data-width="500"></div>""" 
    htmlPost = htmlPost % postdic
    return html_parser.unescape(htmlPost)


def convertTweetToHtml(tweet):
    
    tweetdict = {'username':tweet.twitterpage.username,
                 'name':tweet.twitterpage.name,
                 'message':tweet.message,
                 'tweetid':str(tweet.tweetid),
                 'created_time':str(tweet.created_time),
                 'ftime':str(tweet.created_time)}

    html_parser = HTMLParser.HTMLParser()
        
    htmlTweet = """<blockquote class="twitter-tweet" width="350"><p>%(message)s</p>&mdash; %(name)s (%(username)s) <a href="https://twitter.com/%(username)s/status/%(tweetid)s" data-datetime="%(created_time)s">%(ftime)s</a></blockquote><script src="http://platform.twitter.com/widgets.js" charset="utf-8"></script>""" 
    htmlTweet = htmlTweet % tweetdict
    return html_parser.unescape(htmlTweet)


