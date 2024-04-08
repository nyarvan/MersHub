from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.views.generic import ListView, DetailView, FormView, TemplateView
from cart.cart import Cart
from .models import Product, Category, ProductImages
from .forms import ContactForm


def page_not_found_view(request):
    """
    Render a custom 404 error page.

    This view renders a custom 404 error page when a page is not found.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the rendered 404 error page.

    """
    return render(request, '404.html', status=404)


class Homepage(ListView):
    """
    View class for the homepage.

    This view displays the homepage, including featured products,
    product categories, and a list of products based on filters
    such as discounts, new arrivals, and best sellers.

    Attributes:
        template_name (str): The name of the template used for rendering
    the homepage.
        context_object_name (str): The name of the variable containing
    the product list in the template.

    """
    template_name = 'homepage.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Get the queryset for the list of products.

        Returns:
            queryset: A filtered queryset of products based on filter
        and category parameters.

        """
        type_filter = self.request.GET.get('filter', '')
        category = self.request.GET.get('category', '')

        if type_filter == 'Знижки' and category:
            return Product.objects.filter(
                category__subcategory__slug=category, is_special=True,
                available=True)[:6]
        elif type_filter == 'Знижки':
            return Product.objects.filter(is_special=True, available=True)[:6]
        elif type_filter == 'Новинки' and category:
            return Product.objects.filter(
                category__subcategory__slug__exact=category, new_in=True,
                available=True)[:6]
        elif type_filter == 'Новинки':
            return Product.objects.filter(new_in=True, available=True)[:6]
        elif type_filter == 'Найбільше продаються' and category:
            return Product.objects.filter(
                category__subcategory__slug__exact=category, best_seller=True,
                available=True)[:6]
        elif type_filter == 'Найбільше продаються':
            return Product.objects.filter(best_seller=True, available=True)[:6]
        elif category:
            return Product.objects.filter(
                category__subcategory__slug__exact=category, new_in=True,
                available=True)[:6]
        else:
            return Product.objects.filter(new_in=True, available=True)[:6]

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the view.

        This method retrieves the context data required for rendering the view,
        including the type filter, special products, product categories,
        and shopping cart.

        Args:
            **kwargs: Additional keyword arguments passed to the method.

        Returns:
            dict: A dictionary containing the context variables
        for the template.

        """
        cart = Cart(self.request)
        type_filter = self.request.GET.get('filter', '')
        if not type_filter:
            type_filter = 'Новинки'

        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(
            count=Count('category__product')).filter(subcategory=None)
        context['type_filter'] = type_filter
        context['specials'] = Product.objects.filter(
            is_special=True).order_by('?')[:8]
        context['categories'] = categories
        context['cart'] = cart
        return context


class ProductsListView(ListView):
    """
    View class for listing products.

    This view displays a list of products based on various filters
    and sorting options.

    Attributes:
        template_name (str): The name of the template used for rendering
    the product list.
        context_object_name (str): The name of the variable containing
    the product list in the template.
        paginate_by (int): The number of products per page in pagination.

    """
    template_name = 'products-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """
        Get the queryset for the list of products.

        Returns:
            queryset: A filtered queryset of products based on category,
        price, and sorting parameters.

        """
        category_slug = self.kwargs.get('slug_category')
        price_lte = self.request.GET.get('price_lte')
        if price_lte:
            price_lte = int(price_lte)
        price_gte = self.request.GET.get('price_gte')
        if not price_gte:
            price_gte = 0
        else:
            price_gte = int(price_gte)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            if price_lte and category.subcategory:
                products = Product.objects.filter(
                    category=category, price__lte=price_lte,
                    price__gte=price_gte, available=True)
            elif price_lte and not category.subcategory:
                products = Product.objects.filter(
                    category__subcategory=category, price__lte=price_lte,
                    price__gte=price_gte, available=True)
            elif not category.subcategory:
                products = Product.objects.filter(
                    category__subcategory=category, available=True)
            else:
                products = Product.objects.filter(
                    category=category, available=True)
        elif price_lte:
            products = Product.objects.filter(
                price__lte=price_lte, price__gte=price_gte, available=True)
        else:
            products = Product.objects.all()

        sort_param = self.request.GET.get('sort')
        if sort_param == 'name':
            products = products.order_by('name')
        elif sort_param == 'new-in':
            products = products.order_by('new_in')
        elif sort_param == 'low-price':
            products = products.order_by('price')
        elif sort_param == 'high-price':
            products = products.order_by('-price')
        else:
            products = products.order_by('name')
        return products

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the product list.

        Returns:
            dict: A dictionary containing the context variables
        for the template.

        """
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('slug_category')
        if category:
            context['category'] = Category.objects.values(
                'name').get(slug=category)
        else:
            context['category'] = category
        context['cart'] = cart
        return context


class SearchProductsView(ListView):
    """
    View class for searching products.

    This view allows users to search for products based on their name,
    category, subcategory, or ID.

    Attributes:
        template_name (str): The name of the template used for rendering
    the product list.
        context_object_name (str): The name of the variable containing
    the product list in the template.
        paginate_by (int): The number of products per page in pagination.

    """
    template_name = 'products-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """
        Get the queryset for the list of products.

        Returns:
            queryset: A filtered queryset of products based
        on the search parameter.

        """
        search_param = self.request.GET.get('search')
        return Product.objects.filter(
            Q(name__icontains=search_param) |
            Q(category__name__icontains=search_param) |
            Q(category__subcategory__name__icontains=search_param) |
            Q(id__icontains=search_param), available=True)

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the view.

        Returns:
            dict: A dictionary containing the context variables
        for the template.

        """
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.GET.get('search')
        context['cart'] = cart
        return context


class ProductDetailView(DetailView):
    """
    View class for displaying product details.

    This view displays detailed information about a specific product,
    including its images and similar products.

    Attributes:
        template_name (str): The name of the template used for rendering
    the product detail page.
        context_object_name (str): The name of the variable containing
    the product object in the template.
        model (Model): The model class representing the product.
        queryset (QuerySet): The queryset of products with
    pre-fetched category objects.

    """
    template_name = 'product.html'
    context_object_name = 'product'
    model = Product
    queryset = Product.objects.all().select_related('category')

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the view.

        Returns:
            dict: A dictionary containing the context variables for
        the template.

        """
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        images = ProductImages.objects.filter(product=product)
        products_be_like = Product.objects.exclude(id=product.id)\
            .filter(
                category__subcategory=product.category.subcategory,
                available=True)

        context['images'] = images
        context['products_be_like'] = products_be_like
        context['cart'] = cart
        return context


class ContactView(FormView):
    """
    View class for handling contact form submissions.

    This view displays a contact form for users to submit inquiries,
    and handles form submission by saving the form data.

    Attributes:
        form_class (Form): The form class used for rendering and processing
    the contact form.
        template_name (str): The name of the template used for rendering
    the contact form.
        success_url (str): The URL to redirect to
    after successful form submission.

    """
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = '/contact-us/'

    def form_valid(self, form):
        """
        Process a valid form submission.

        This method is called when the submitted form data is valid.
        It saves the form data and returns a redirect response.

        Args:
            form (Form): The validated form instance.

        Returns:
            HttpResponseRedirect: A redirect response to the success URL.

        """
        form.save()
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the view.

        Returns:
            dict: A dictionary containing the context variables for
        the template.

        """
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context


class AboutUsView(TemplateView):
    """
    View class for displaying the about us page.

    This view displays information about the company or website.

    Attributes:
        template_name (str): The name of the template used for rendering
    the about us page.

    """
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the view.

        Returns:
            dict: A dictionary containing the context variables for
        the template.

        """
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context


class DeliveryPaymentView(TemplateView):
    """
    View class for displaying the delivery and payment information page.

    This view displays information about delivery options and payment methods.

    Attributes:
        template_name (str): The name of the template used for rendering
    the delivery and payment page.

    """

    template_name = 'delivery-payment.html'

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the view.

        Returns:
            dict: A dictionary containing the context variables for
        the template.

        """
        cart = Cart(self.request)

        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context


class GuaranteeView(TemplateView):
    """
    View class for displaying the guarantee information page.

    This view displays information about product guarantees and warranties.

    Attributes:
        template_name (str): The name of the template used for rendering
    the guarantee page.

    """

    template_name = 'guarantee.html'

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the view.

        Returns:
            dict: A dictionary containing the context variables for
        the template.

        """
        cart = Cart(self.request)

        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context
