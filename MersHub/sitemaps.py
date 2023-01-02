from django.contrib import sitemaps
from shop.models import Category, Product


class AbstractSitemapClass:
    changefreq = 'daily'
    url = None

    def get_absolute_url(self):
        return self.url


class StaticViewSitemap(sitemaps.Sitemap):
    pages = {
        'home': '/',  # Add more static pages here like this 'example':'url_of_example',
        'contact': '/contact-us/',
        'about-us': '/about-us/',
        'delivery-payment': '/delivery-payment/',
        'guarantee': '/guarantee/'
    }
    main_sitemaps = []
    for page in pages.keys():
        sitemap_class = AbstractSitemapClass()
        sitemap_class.url = pages[page]
        main_sitemaps.append(sitemap_class)

    def items(self):
        return self.main_sitemaps

    priority = 1
    changefreq = "yearly"


class CategorySitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()


class ProductSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Product.objects.filter(available=True)

    def lastmod(self, obj):
        return obj.created
