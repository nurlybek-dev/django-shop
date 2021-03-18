from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView
from .models import Category, Order, OrderProduct, Product, Cart, Review
from .forms import OrderForm, ReviewForm


class ShopListView(ListView):
    model = Category
    template_name = 'shop/shop_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['can_write_review'] = Review.objects.filter(user=self.request.user, product=context['product']).count() == 0
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_detail', args=[str(self.kwargs['pk'])])

    def post(self, request, *args, **kwargs):
        exists = Review.objects.filter(user=self.request.user, product=self.kwargs['pk'])
        if exists:
            print(exists)
            return redirect(self.get_success_url())
        return super().post(request, *args, **kwargs)


class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart/cart_list.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = sum(item.product.price for item in context['object_list'])
        context['order_form'] = OrderForm()
        return context

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).all()


class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = Cart
    template_name = 'cart/cart_delete.html'
    success_url = reverse_lazy('cart_list')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(product=product, user=request.user)
    cart.save()
    return_path = request.META.get('HTTP_REFERER', '/')
    return redirect(return_path)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'
    ordering = '-order_time'


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_create.html'
    # fields = ['delivery_address', 'contact_phone']

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        cart = self.request.user.cart.all()
        for c in cart:
            order_product = OrderProduct(order=self.object, product=c.product)
            order_product.save()
            c.delete()

        return HttpResponseRedirect(self.get_success_url())

    def render_to_response(self, context, **response_kwargs):
        cart_count = self.request.user.cart.count()
        if cart_count == 0:
            return redirect(reverse('order_list'))
    
        return super().render_to_response(context, **response_kwargs)


def order_cancel(request, pk):
    order = Order.objects.get(pk=pk)
    if order.status != 1:
        return redirect(reverse('order_list'))

    if request.method == 'POST':
        order.cancel()
        return redirect(reverse('order_list'))

    return render(request, 'order/order_cancel.html')
