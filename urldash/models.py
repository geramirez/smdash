from django.db import models


class Url(models.Model):
        url = models.URLField(primary_key=True)
        is_short = models.NullBooleanField( blank=True, null=True)
        shorttype = models.CharField(max_length = 20, blank=True, null=True)
        shorturl = models.URLField( blank=True, null=True)
        longurl = models.URLField( blank=True, null=True)

        def __unicode__(self):
                url = self.url
                if url == None:
                        url = "NA"
		
		elif len(url) > 40:
			url = url[:40]

		return u'%s' % (url)
