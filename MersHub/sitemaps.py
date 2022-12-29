from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['shop.homepage', 'shop.contact', 'shop.about-us', 'shop.delivery-payment', 'shop.guarantee']

    def location(self, item):
        return reverse(item)
