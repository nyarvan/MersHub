from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from .sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('order.urls', namespace='order')),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('sitemap.xml', sitemap,
         {'sitemaps': {'static': StaticViewSitemap,
                       'category': CategorySitemap,
                       'products': ProductSitemap}},
         name='django.contrib.sitemaps.views.sitemap'),

]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
