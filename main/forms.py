from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime
from twitterdash.models import TwitterPage
from facebookdash.models import FacebookPage

#set defaults
YEAR_RANGE = range(2011, datetime.date.today().year+1)
SEARCH_TYPES=[('boolean','boolean (default)'),('regex','regex (advanced)')]
TIMEPERIODCHOICES=[(datetime.date.today(),'Today'),
                   (datetime.date.today()-datetime.timedelta(days=3),'Last 3 Days',),
                   (datetime.date.today()-datetime.timedelta(days=7),'Last 7 Days'),
                   (datetime.date.today()-datetime.timedelta(days=30),'Last 30 Days')]

PLATFORMS = [('facebook','Facebook'),('twitter','Twitter')]

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

class TopTenFormFacebook(forms.Form):
    firstday = forms.DateField(widget=SelectDateWidget(years=YEAR_RANGE),label="Between (First Day)")
    lastday = forms.DateField(widget=SelectDateWidget(years=YEAR_RANGE),label="Between (Last Day)")

    #OPEN QUERY SETS
    facebookpages = FacebookPage.objects.all().order_by('name')

    facebookpageids = forms.ModelMultipleChoiceField(queryset = facebookpages,
                                                     label="Facebook Pages",
                                                     required = False,
                                                     help_text = "Leave blank to select all <br>")

    keyword = forms.CharField(widget=forms.TextInput,max_length=100,required = False)
    '''
    countries = FacebookPage.objects.values('country').order_by('country').distinct()

    countryids = forms.ModelMultipleChoiceField(queryset = countries,
                                                    label="Countries",
                                                    required = False,
                                                    help_text = "Leave blank to select all <br>" )


    regions = FacebookPage.objects.values('bureau').order_by('bureau').distinct()

    regionids = forms.ModelMultipleChoiceField(queryset = regions,
                                                    label="Regions",
                                                    required = False,
                                                    help_text = "Leave blank to select all <br>" )



    cities = FacebookPage.objects.values('city').order_by('city').distinct()

    cityids = forms.ModelMultipleChoiceField(queryset = cities,
                                                    label="city",
                                                    required = False,
                                                    help_text = "Leave blank to select all <br>" )
     '''
class TopTenFormTwitter(forms.Form):
    firstday = forms.DateField(widget=SelectDateWidget(years=YEAR_RANGE),label="Between (First Day)")
    lastday = forms.DateField(widget=SelectDateWidget(years=YEAR_RANGE),label="Between (Last Day)")

    twitterpages = TwitterPage.objects.all().order_by('name')


    twitterpageids = forms.ModelMultipleChoiceField(queryset = twitterpages,
                                                    label="Twitter Pages",
                                                    required = False,
                                                    help_text = "Leave blank to select all <br>" )

    keyword = forms.CharField(widget=forms.TextInput,max_length=100,required = False)
    '''
    countries = TwitterPage.objects.get_countries()


    countryids = forms.ModelMultipleChoiceField(queryset = countries,
                                                    label="Countries",
                                                    required = False,
                                                    help_text = "Leave blank to select all <br>" )


    regions = TwitterPage.objects.get_bureaus()

    regionids = forms.ModelMultipleChoiceField(queryset = regions,
                                                    label="Regions",
                                                    required = False,
                                                    help_text = "Leave blank to select all <br>" )



    cities = TwitterPage.objects.get_cities()

    cityids = forms.ModelMultipleChoiceField(queryset = cities,
                                                    label="city",
                                                    required = False,
                                                    help_text = "Leave blank to select all <br>" )

    '''

