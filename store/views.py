
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from .models import *
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        customer = Customer.objects.create(customer=user,name=str(first_name)+" "+str(last_name) ,email=email)
        customer.save()
        instance_login = authenticate(request, username=username, password=password)
        
        if instance_login is not None:
            login(request, instance_login)
            return redirect("store")
    return render(request, "store/register.html", {})

def logout_view(request):
    logout(request)
    return redirect("login")

def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("store")
        else:
            redirect("login")
    context = {}
    return render(request, "store/login.html", context)


def store(request, *args, **kwargs):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "store/store.html", context)


def cart(request, *args, **kwargs):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        for i in items:
            print(len(items))
            # if i.quantity == 2:
            #     item = OrderItem.objects.get(id = i.id)
            #     item.delete()
            #     print(i.quantity)
        
    else:
        items = []
        order = {'get_total_items':0, 'get_total_items_price':0}
    context = {"items": items, "order":order}
    return render(request, "store/cart.html", context)


def check_out(request, *args, **kwargs):
   
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        print(items[1])
    else:
        items = []
        order = {'get_total_items':0, 'get_total_items_price':0}
    context = {"items": items, "order":order}
    return render(request, "store/checkout.html", context)


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    loopCount = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        for i in items:
            if product == i.product:
                print(product, " co value giong nhau")
                i.quantity = int(i.quantity) + 1
                i.save()
                break
            else:
                loopCount = loopCount + 1
        
        if loopCount == len(items):
            item = OrderItem.objects.create(product=product, order=order)
            item.save()
        # continue
        
    else:
        items = []
        order = {'get_total_items': 0, 'get_total_items_price': 0}
    context = {"items": items, "order": order}
    return redirect("cart")




