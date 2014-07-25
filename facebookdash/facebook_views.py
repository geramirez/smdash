from django.shortcuts import render
from django.http import HttpResponse
from facebookdash.models import FacebookPost
import datetime
import HTMLParser

def search_form(request):
    return render(request, 'search_form.html')
	
def search(request):
    errors = []
    if 'q' in request.GET:
		q = request.GET['q']
        
		if not q:
			errors.append('Enter a search term.')
		elif len(q) > 20:
			errors.append('Please enter at most 20 characters.')	
		else:
			posts = FacebookPost.objects.filter(message__iregex=q)

			posts = [x for x in posts if x.fuzzy_serach("The world is watching reports of a downed passenger jet near the Russia-Ukraine border Our thoughts and prayers are with all the families of the passengers, wherever they call home.")]
			
			return render(request, 'search_results.html',
					{'posts': posts, 'query': q})
		
    return render(request, 'search_form.html',
        {'error': errors})

def topten_fbposts(request):
    #gets the top 10 and formats them

    #get the dates
    enddate = datetime.date.today()
    startdate = enddate - datetime.timedelta(days=7)

    #make query
    posts = FacebookPost.objects.filter(created_time__range=[startdate, enddate])\
                                .extra(select = {'fieldsum':'likes + shares + comments'}, order_by = ('-fieldsum',))[0:10]

    PostsHTML = []

    for post in posts:
        PostsHTML.append(convertPostToHtml(post))
       
    return render(request, 'top_10_facebook.html',
                  {'posts':PostsHTML})


def convertPostToHtml(post):
    
    postdic = {"username":post.facebookpage.username,
               "postid":post.postid.split("_")[1]}

    html_parser = HTMLParser.HTMLParser()
        
    htmlPost = """<div class="fb-post" data-href="https://www.facebook.com/%(username)s/posts/%(postid)s" data-width="500"></div>""" 
    htmlPost = htmlPost % postdic
    return html_parser.unescape(htmlPost)


