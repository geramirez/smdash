from django.contrib import admin

# Register your models here.
from mailchimpdash.models import Email, EmailTweets, EmailFacebookPosts



admin.site.register(Email)
admin.site.register(EmailTweets)
admin.site.register(EmailFacebookPosts)

