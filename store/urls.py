from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static

from django.conf import settings
from .views import *

urlpatterns = [
    path("home2/",Home2.as_view(), name="home2"),
    path("", Home.as_view(), name="store"),
    path("cart/", cart, name="cart"),
    path("detail/<str:id>/", product_detail, name="detail"),
    path("checkout/", check_out, name="checkout"),
    path("add/<str:id>/", add_to_cart, name="add"),
    path("decrease/<str:id>/", decrease_from_cart, name="decrease"),
    path("checkshipping/<str:id>/", check_shipping, name="shipped"),
    path('login/', login_page, name="login"),
    path('logout/', logout_view, name="logout"),
    path("register/", register, name="register"),
    path("addnew/",CreateView.as_view(), name="addproduct"),
    path("info/", InfoView.as_view(), name="info"),
    path("confirm/<str:id>/", confirm, name="confirm"),
    path("available/<str:id>/", available, name="available"),
    path("ushipping/", MyShipping.as_view(), name="usershipping")
]

