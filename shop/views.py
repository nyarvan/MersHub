from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.views.generic import ListView, DetailView, FormView, TemplateView
from .models import Product, Category, ProductImages
from .forms import ContactForm
from cart.cart import Cart


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


class Homepage(ListView):
    template_name = 'homepage.html'
    context_object_name = 'products'

    def get_queryset(self):
        type_filter = self.request.GET.get('filter', '')
        category = self.request.GET.get('category', '')

        if type_filter == 'Знижки' and category:
            return Product.objects.filter(category__subcategory__slug=category, is_special=True)[:6]
        elif type_filter == 'Знижки':
            return Product.objects.filter(is_special=True)[:6]
        elif type_filter == 'Новинки' and category:
            return Product.objects.filter(category__subcategory__slug__exact=category, new_in=True)[:6]
        elif type_filter == 'Новинки':
            return Product.objects.filter(new_in=True)[:6]
        elif type_filter == 'Найбільше продаються' and category:
            return Product.objects.filter(category__subcategory__slug__exact=category, best_seller=True)[:6]
        elif type_filter == 'Найбільше продаються':
            return Product.objects.filter(best_seller=True)[:6]
        elif category:
            return Product.objects.filter(category__subcategory__slug__exact=category, is_special=True)[:6]
        else:
            return Product.objects.filter(is_special=True)[:6]

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(self.request)
        type_filter = self.request.GET.get('filter', '')
        if not type_filter:
            type_filter = 'Знижки'

        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(count=Count('category__product')).filter(subcategory=None)
        context['type_filter'] = type_filter
        context['specials'] = Product.objects.filter(is_special=True).order_by('?')[:8]
        context['categories'] = categories
        context['cart'] = cart
        return context


class ProductsListView(ListView):
    template_name = 'products-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
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
                products = Product.objects.filter(category=category, price__lte=price_lte, price__gte=price_gte)
            elif price_lte and not category.subcategory:
                products = Product.objects.filter(category__subcategory=category, price__lte=price_lte, price__gte=price_gte)
            elif not category.subcategory:
                products = Product.objects.filter(category__subcategory=category)
            else:
                products = Product.objects.filter(category=category)
        elif price_lte:
            products = Product.objects.filter(price__lte=price_lte, price__gte=price_gte)
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

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('slug_category')
        if category:
            context['category'] = Category.objects.values('name').get(slug=category)
        else:
            context['category'] = category
        context['cart'] = cart
        return context


class SearchProductsView(ListView):
    template_name = 'products-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        search_param = self.request.GET.get('search')
        return Product.objects.filter(Q(name__icontains=search_param) | Q(category__name__icontains=search_param) |
                                      Q(category__subcategory__name__icontains=search_param) | Q(id__icontains=search_param))

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['category'] = self.request.GET.get('search')
        context['cart'] = cart
        return context


class ProductDetailView(DetailView):
    template_name = 'product.html'
    context_object_name = 'product'
    model = Product
    queryset = Product.objects.all().select_related('category')

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        images = ProductImages.objects.filter(product=product)
        products_be_like = Product.objects.exclude(id=product.id)\
            .filter(category=product.category)

        context['images'] = images
        context['products_be_like'] = products_be_like
        context['cart'] = cart
        return context


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = '/contact-us/'

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context


class AboutUsView(TemplateView):
    template_name = 'about-us.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context


class DeliveryPaymentView(TemplateView):
    template_name = 'delivery-payment.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context


class GuaranteeView(TemplateView):
    template_name = 'guarantee.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context['cart'] = cart
        return context
