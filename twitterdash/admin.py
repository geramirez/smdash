from django.contrib import admin

#register models here
from twitterdash.models import TwitterPage, TwitterTweet, TwitterPublicStat

#add the names we would like listed

class TwitterPageAdmin(admin.ModelAdmin):
    list_display = ('name','username','pageid',)
    search_fields = ('name','username',)

class TwitterTweetsAdmin(admin.ModelAdmin):
    list_display = ('twitterpage','message','retweets','favorites',)
    search_fields = ('twitterpage__username','message',)
    ist_filter = ('created_time',)
    date_hierarchy = 'created_time'
    ordering = ('-created_time',)

class TwitterPublicStatAdmin(admin.ModelAdmin):
    list_display = ('twitterpage','date','followers','following',)


admin.site.register(TwitterPage, TwitterPageAdmin)
admin.site.register(TwitterTweet, TwitterTweetsAdmin)
admin.site.register(TwitterPublicStat, TwitterPublicStatAdmin)

