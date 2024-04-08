from typing import Optional
from django.contrib.sitemaps import Sitemap
from shop.models import Category, Product


class AbstractSitemapClass:
    """
    Abstract base class for sitemap classes.

    This class defines common attributes and methods for sitemap classes.

    Attributes:
        changefreq (str): The change frequency of the URL. Defaults to 'daily'.
        url (str): The absolute URL of the resource.

    """

    changefreq = 'daily'
    url: Optional[str] = None

    def get_absolute_url(self):
        """
        Method to get the absolute URL of the resource.

        Returns:
            str: The absolute URL of the resource.

        """

        return self.url


class StaticViewSitemap(Sitemap):
    """
    Sitemap class for static views.

    This class generates sitemap entries for static views.

    Attributes:
        pages (dict): A dictionary containing static page URLs.
        main_sitemaps (list): A list containing instances of
    AbstractSitemapClass for each static page.

    """

    pages = {
        'home': '/',
        'contact': '/contact-us/',
        'about-us': '/about-us/',
        'delivery-payment': '/delivery-payment/',
        'guarantee': '/guarantee/'
    }

    main_sitemaps = []
    for page, url in pages.items():
        sitemap_class = AbstractSitemapClass()
        sitemap_class.url = url
        main_sitemaps.append(sitemap_class)

    def items(self):
        """
        Method to return sitemap items.

        Returns:
            list: The list of sitemap items.

        """

        return self.main_sitemaps

    priority = 1
    changefreq = "yearly"


class CategorySitemap(Sitemap):
    """
    Sitemap class for category objects.

    This class generates sitemap entries for category objects.

    Attributes:
        changefreq (str): The change frequency of the URLs.
    Defaults to "weekly".
        priority (float): The priority of the URLs. Defaults to 0.5.

    """

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        """
        Method to return category items for the sitemap.

        Returns:
            QuerySet: A queryset containing all category objects.

        """

        return Category.objects.all()


class ProductSitemap(Sitemap):
    """
    Sitemap class for product objects.

    This class generates sitemap entries for product objects.

    Attributes:
        changefreq (str): The change frequency of the URLs. Defaults to "daily".
        priority (float): The priority of the URLs. Defaults to 0.6.

    """

    changefreq = "daily"
    priority = 0.6

    def items(self):
        """
        Method to return product items for the sitemap.

        Returns:
            QuerySet: A queryset containing all available product objects.

        """

        return Product.objects.filter(available=True)

    def lastmod(self, obj):
        """
        Method to get the last modification date of a product.

        Args:
            obj: The product object.

        Returns:
            datetime: The last modification date of the product.

        """

        return obj.created
