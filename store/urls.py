from django.urls import path
from .views import *

urlpatterns = [
    path("", store, name="store"),
    path("cart/", cart, name="cart"),
    path("checkout/", check_out, name="checkout"),
    path("add/<str:id>/", add_to_cart, name="add"),
    path('login/', login_page, name="login"),
    path('logout/', logout_view, name="logout"),
    path("register/", register, name="register"),
]