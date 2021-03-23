from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from django.conf import settings

import hashlib
import time


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])

    def get_head_products(self):
        return self.products.all()[:5]

def product_cover_path(instance, filename):
    hash_object  = hashlib.md5(filename.encode() + str(time.time()).encode())
    name = hash_object.hexdigest()
    format = filename.split('.')[-1]
    return 'covers/{0}.{1}'.format(name, format)

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField(default=0)
    description = models.TextField(default='', blank=True, null=False)
    cover = models.ImageField(upload_to=product_cover_path, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    def get_image_url(self):
        if self.cover:
            return self.cover.url
        else:
            return settings.STATIC_URL + 'images/no-photo.png'

    def get_avg_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        if avg == None:
            return 0
        return int(avg)


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart')


order_statuses = [
    (1, 'Обрабатывается'),
    (2, 'Подтвержден'),
    (3, 'Оплачен'),
    (4, 'Отправлен'),
    (5, 'Доставлен'),
    (6, 'Отменен')
]

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    order_time = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=12)
    status = models.SmallIntegerField(choices=order_statuses, default=1)

    def __str__(self):
        return '<Order №%d>' % self.id

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])

    def get_total_price(self):
        return sum(item.product.price for item in self.products.all())

    def cancel(self):
        self.status = 6
        self.save()
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return self.product.name


rating_values = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    rating = models.SmallIntegerField(choices=rating_values)
    comment = models.TextField(blank=True, null=False, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
