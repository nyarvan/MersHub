from django.urls import path, include
from shop.views import Homepage, ProductsListView, SearchProductsView, \
    ProductDetailView, ContactView, AboutUsView, \
    DeliveryPaymentView, GuaranteeView

app_name = 'shop'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('contact-us/', ContactView.as_view(), name='contact'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path(
        'delivery-payment/', DeliveryPaymentView.as_view(),
        name='delivery-payment'),
    path('guarantee/', GuaranteeView.as_view(), name='guarantee'),
    path('shop/', ProductsListView.as_view(), name='products'),
    path('search/', SearchProductsView.as_view(), name='search'),
    path(
        'shop/<slug:slug_category>/', ProductsListView.as_view(),
        name='products_by_category'),
    path('shop/<slug:slug>', ProductDetailView.as_view(), name='product')
]

handler404 = "shop.views.page_not_found_view"
