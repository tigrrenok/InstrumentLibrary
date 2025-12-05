from django.contrib.sitemaps import Sitemap

from Instruments.models import Instrument, InstrumentCategory


class InstrumentSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Instrument.published_objects.all()

    def lastmod(self, obj):
        return obj.time_updated

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return InstrumentCategory.objects.all()


