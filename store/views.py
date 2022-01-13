
from django.db.models.fields import NullBooleanField
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.views.generic import *
from django.contrib.auth.views import *
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProductForm
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
    return render(request, "store/home.html", context)


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

def product_detail(request,id , *arg, **kwargs):
    product = Product.objects.get(id = id)
    products = Product.objects.filter(available=True)
    context = {"product":product, "products":products}
    return render(request, "store/single-product.html", context)

def promotion_detail(request,id , *arg, **kwargs):
    promotion = Promotion.objects.get(id = id)
    promotions = Promotion.objects.all()
    context = {"promotion":promotion, "promotions":promotions}
    return render(request, "store/single-news.html", context)


def check_out(request, *args, **kwargs):
   
    
    if request.user.is_authenticated:
        
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        if request.method == "POST":
            address = request.POST["address"]
            city = request.POST["city"]
            state = request.POST["state"]
            address = request.POST["address"]
            for i in items:
                shipping, created = ShippingAddress.objects.get_or_create(customer=customer, order = order, seller = i.seller, shippingstatus = False )
                shipping.address = address
                shipping.city = city
                shipping.district = state
                shipping.product.add(i.product)
                shipping.orderitems.add(i)
                shipping.save()
            
            order.completed=True
            order.save()
            return redirect("store")
            
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
            item = OrderItem.objects.create(product=product, order=order, seller = product.seller)
            item.save()
        # continue
        
    else:
        items = []
        order = {'get_total_items': 0, 'get_total_items_price': 0}
    context = {"items": items, "order": order}
    return redirect("cart")

def decrease_from_cart(request, id):
    product = Product.objects.get(id=id)
    loopCount = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        for i in items:
            if product == i.product:
                if i.quantity > 1:
                    print(product, " co value giong nhau")
                    i.quantity = int(i.quantity) - 1
                    i.save()
                    break
                else:
                    i.delete()
            else:
                loopCount = loopCount + 1
        
        if loopCount == len(items):
            item = OrderItem.objects.create(product=product, order=order, seller = product.seller)
            item.save()
        # continue
        
    else:
        items = []
        order = {'get_total_items': 0, 'get_total_items_price': 0}
    context = {"items": items, "order": order}
    return redirect("cart")

def check_shipping(request, id):
    orderitem = OrderItem.objects.get(id=id)
    if request.user.is_authenticated:
        print("alo")
        print(orderitem.shippingstatus)
        orderitem.shippingstatus = None
        orderitem.save()
         
    return redirect("usershipping")

class CreateView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = "store/add.html"
    success_url = reverse_lazy("store")
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super(CreateView, self).form_valid(form)

class InfoView(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/info.html"
    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        # context['videos'] = (v for v in Video.objects.all())
        context['product'] = Product.objects.filter(seller = self.request.user)
        context['shipping'] = ShippingAddress.objects.filter(seller = self.request.user, shippingstatus = False)
        context['shipped'] = ShippingAddress.objects.filter(seller = self.request.user, shippingstatus = True)
        context['order'] = Order.objects.filter(completed = True)
        context['orderitems'] = OrderItem.objects.filter(seller = self.request.user, order_id__in = [o for o in context['order']])
        for i in context['orderitems']:
                print(i.product)
        return context

class Home(LoginRequiredMixin, ListView):
    model = Product
    queryset = Product.objects.filter(available=True)
    context_object_name = "products"
    template_name = "store/index.html"
    paginate_by = 3
    ordering = 'name'
    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['top'] = Product.objects.get(price= 999)
        context['news'] = Promotion.objects.all()
        return context

class Home2(LoginRequiredMixin, ListView):
    model = Product
    queryset = Product.objects.filter(available=True)
    context_object_name = "products"
    template_name = "store/index_2.html"
    paginate_by = 3
    ordering = 'name'

def confirm(request, id):
    shipping = ShippingAddress.objects.get(id=id)
    if request.user.is_authenticated:
        if request.user == shipping.seller:
            print(shipping.seller , " da kiem tra don van chuyen co id ", shipping.id, " cho khach hang ", shipping.customer)
            shipping.shippingstatus = True
            shipping.save()
    return redirect("info")

def available(request, id):
    product = Product.objects.get(id = id)
    if request.user.is_authenticated:
        if request.user == product.seller:
            if product.available == True:
                product.available = False
            else:
                product.available = True
        product.save()
    return redirect("info")

class MyShipping(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = "products"
    template_name = "store/usershipping.html"
    def get_context_data(self, **kwargs):
        context = super(MyShipping, self).get_context_data(**kwargs)
        customer = Customer.objects.get(customer= self.request.user)
        context['orders'] = Order.objects.filter(customer = customer, completed = True)
        # orders = Order.objects.filter(customer = customer)
        context['orderitems'] = OrderItem.objects.filter(order_id__in =[o for o in context['orders']], shippingstatus = False )
        context['ordereditems'] = OrderItem.objects.filter(order_id__in =[o for o in context['orders']], shippingstatus = None )
        return context
