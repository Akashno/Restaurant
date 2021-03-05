from django.urls import path
from main.views import *

urlpatterns = [
    path('', index, name='index'),
    path('products/', products, name='products'),
    path('profile/', profile, name='profile'),
    path('addcart/<str:pk>', add_cart, name='add_cart'),
    path('deletecart/<str:pk>', delete_cart, name='delete_cart'),
    path('emptycart/', empty_cart, name='empty_cart'),
    path('order/', add_order, name='add_order'),
    path('deleteorder/<str:pk>', delete_order, name='delete_order'),
    path('table/', table, name='table'),
    path('addreservation/<str:pk>', add_reservation, name='add_reservation'),

    path('payment/', payment, name='payment'),

    path('register/', register, name='register'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),

    path('admin_page/', admin_page, name='admin_page'),
    path('admin_approval/<str:pk>', admin_approval, name='admin_approval'),

]