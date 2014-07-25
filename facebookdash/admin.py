from django.contrib import admin

# Register your models here.
from facebookdash.models import FacebookPage, FacebookPost, FacebookPublicStat

#add the names we would like listed
class FacebookPostAdmin(admin.ModelAdmin):
	list_display = ('facebookpage','created_time','kind')
	search_fields = ('facebookpage','message')
	ist_filter = ('created_time',)
	date_hierarchy = 'created_time'
	ordering = ('-created_time',)

class FacebookPageAdmin(admin.ModelAdmin):
	list_display = ('name','department','bureau','country','city',)
	search_fields = ('name','username','pageid',)

class FacebookPublicStatAdmin(admin.ModelAdmin):
	list_display = ('facebookpage','date','followers','ptats')
	search_fields = ('facebookpage',)
	list_filter = ('date',)
	date_hierarchy = 'date'
	ordering = ('-date',)


admin.site.register(FacebookPost, FacebookPostAdmin)
admin.site.register(FacebookPage, FacebookPageAdmin)
admin.site.register(FacebookPublicStat, FacebookPublicStatAdmin)
