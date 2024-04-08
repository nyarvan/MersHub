from django.views.generic import FormView, TemplateView
from cart.cart import Cart
from .forms import CreateOrderForm
from .models import OrderItem


class OrderView(FormView):
    """
    View for processing orders.

    This view handles the creation of orders based on form submissions.
    Upon successful submission, it saves the order and clears the cart.

    Attributes:
        template_name (str): The name of the template to render.
        form_class (Form): The form class to use for order creation.
        success_url (str): The URL to redirect to after successful form
    submission.

    """

    template_name = 'order.html'
    form_class = CreateOrderForm
    success_url = 'success/'

    def form_valid(self, form):
        """
        Method called when form submission is valid.

        This method saves the order based on the submitted form data and
        clears the cart.

        Args:
            form (Form): The validated form instance.

        Returns:
            HttpResponse: The HTTP response.

        """

        cart = Cart(self.request)
        order = form.save()
        for item in cart:
            OrderItem.objects.create(
                order=order, product=item['product'],
                price=int(item['price']), count=item['count'])
        cart.clear()
        return super(OrderView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Method to get additional context data.

        This method adds the cart to the context.

        Returns:
            dict: The context data.

        """

        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context


class SuccessOrderView(TemplateView):
    """
    View for displaying success message after order submission.

    This view renders a success message template upon successful
    order submission.

    Attributes:
        template_name (str): The name of the template to render.

    """

    template_name = 'success.html'
