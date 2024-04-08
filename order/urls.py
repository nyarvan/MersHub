from django.urls import path
from .views import OrderView, SuccessOrderView

app_name = 'order'

urlpatterns = [
    path('checkout/', OrderView.as_view(), name='checkout'),
    path('checkout/success/', SuccessOrderView.as_view(), name='success-order')
]
