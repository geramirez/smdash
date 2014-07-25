from django.contrib import admin

# Register your models here.
from urldash.models import Url

class UrlAdmin(admin.ModelAdmin):
    list_display = ('url','is_short','shorttype','shorturl','longurl')

admin.site.register(Url, UrlAdmin)
