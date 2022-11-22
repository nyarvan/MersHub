from django.views.generic import FormView, TemplateView
from .forms import CreateOrderForm
from cart.cart import Cart
from .models import OrderItem


class OrderView(FormView):
    template_name = 'order.html'
    form_class = CreateOrderForm
    success_url = 'success/'

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save()
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=int(item['price']),
                                     count=item['count'])
        cart.clear()
        return super(OrderView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context


class SuccessOrderView(TemplateView):
    template_name = 'success.html'
