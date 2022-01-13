from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.expressions import F

# Create your models here.
class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    category = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return self.category



class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    price = models.FloatField(null=True)
    available = models.BooleanField(default=True, null=True, blank=False)
    image = models.ImageField()
    seller = models.ForeignKey(User, on_delete=CASCADE, null=True)
    tag = models.ManyToManyField(Category, related_name="tag_product", blank=True)
    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def get_total_items_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total_price for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    shippingstatus = models.BooleanField(default=False, null=True, blank=False)
    added_date = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=CASCADE, null=True )

    def __str__(self):
        return str(str(self.quantity)+" "+str(self.product))+ " of Order with id "+ str(self.order.id)
    @property
    def get_total_price(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order,  on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, default=" ")
    district = models.CharField(max_length=55, null=True, default=" ")
    city = models.CharField(max_length=55, null=True, default=" ")
    added_date = models.DateTimeField(auto_now_add=True)
    shippingstatus = models.BooleanField(default=False, null=True, blank=False)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_seller")
    product = models.ManyToManyField(Product, related_name="shipping_product", blank=True)
    orderitems = models.ManyToManyField(OrderItem, related_name="shipping_item", blank=True)

    def __str__(self):
        return str(self.order)


class Promotion(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=CASCADE, null= False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    tag = models.ManyToManyField(Category, related_name="tag_cate" , blank=True)
    content = models.TextField(null= False, blank=False)
    picture = models.ImageField()
    def __str__(self):
        return self.title