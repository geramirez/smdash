from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#import from main app
from main.views import CampaignSearch,ContentSearch,TopTenFacebook,TopTenTwitter

#facebookdash imports
from facebookdash.corefunctions import update_facebook_posts, update_facebook_pages
from facebookdash import facebook_views

#twitterdash imports
from twitterdash.corefunctions import update_twitter_pages, update_twitter_posts
from twitterdash import twitter_views

#mailchimp imports
from mailchimpdash import mailchimp_views

urlpatterns = patterns('',
            #admin
	    url(r'^admin/', include(admin.site.urls)),
            #twitter
	    url(r'^search_twitter/$', twitter_views.search),
	    url(r'^update_twitter_posts/$', update_twitter_posts.update),
	    url(r'^update_twitter_page_stats/$', update_twitter_pages.update),
	    url(r'^load_twitter_pages/$', update_twitter_pages.load),
            url(r'^top_ten_tweets/$', twitter_views.topten_tweets),
            #facebook                       
	    url(r'^search_facebook/$', facebook_views.search),
	    url(r'^update_facebook_posts/$', update_facebook_posts.update),
	    url(r'^load_facebook_pages/$', update_facebook_pages.load),
	    url(r'^update_facebook_page_stats/$', update_facebook_pages.update_facebook_page_stats), 
            url(r'^top_ten_facebook_posts/$', facebook_views.topten_fbposts),

            #campaign_search
            url(r'^campaign_search/$', CampaignSearch),
            url(r'^content_search/$',ContentSearch),
            url(r'^topten/facebook$',TopTenFacebook),
            url(r'^topten/twitter$',TopTenTwitter),

            #Mailchimp
            url(r'^Mailchimpupdate/$',mailchimp_views.UpdateMailchimp),
            url(r'^MailChimp-Twitter/$',mailchimp_views.UpdateTweets),
            url(r'^Mailchimp-Report/$',mailchimp_views.MailchimpReport),
            url(r'^Mailchimp-Imageupdate/$',mailchimp_views.UpdateImages),

)
