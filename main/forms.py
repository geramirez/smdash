from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

#set defaults
YEAR_RANGE = range(2011, datetime.date.today().year+1)
SEARCH_TYPES=[('boolean','boolean (default)'),('regex','regex (advanced)')]

class CampaignSearchForm(forms.Form):
    firstday = forms.DateField(widget=SelectDateWidget(years=YEAR_RANGE),label="Campaign Start Date")
    lastday = forms.DateField(widget=SelectDateWidget(years=YEAR_RANGE),label="Campaign End Date")
    #searchtype = forms.ChoiceField(choices=SEARCH_TYPES, widget=forms.RadioSelect(),label="Type of search")
    keyword = forms.CharField(widget=forms.TextInput,max_length=100)
    #urls = forms.CharField(widget=forms.TextInput,max_length=100,required = False)

class ContentSearchForm(forms.Form):
    firstday = forms.DateField(widget=SelectDateWidget(years=YEAR_RANGE),label="Campaign Start Date")
    lastday = forms.DateField(widget=SelectDateWidget(years=YEAR_RANGE),label="Campaign End Date")
    #searchtype = forms.ChoiceField(choices=SEARCH_TYPES, widget=forms.RadioSelect(),label="Type of search")
    keyword = forms.CharField(widget=forms.Textarea)
    #urls = forms.CharField(widget=forms.TextInput,max_length=100,required = False)
