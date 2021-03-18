from django.urls import path

from .views import ( 
    CartDeleteView,
    CartListView, 
    ShopListView, 
    CategoryDetailView, 
    ProductDetailView, 
    CreateReviewView,
    add_to_cart,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    order_cancel
    )


urlpatterns = [
    path('', ShopListView.as_view(), name='home'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/create-review/', CreateReviewView.as_view(), name='create_review'),

    path('cart/', CartListView.as_view(), name='cart_list'),
    path('cart/<int:pk>/delete', CartDeleteView.as_view(), name='cart_delete'),
    path('cart/add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/order-cancel', order_cancel, name='order_cancel'),
    path('orders/create-order', OrderCreateView.as_view(), name='create_order'),
]
