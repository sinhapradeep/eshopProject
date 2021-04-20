from django.urls import path
from .views import Index, Cart , Checkout, Orderview
from cart import views

urlpatterns = [
      path('', Index.as_view(), name='index'),
      path('Index/', Index.as_view(), name='Index'),
      path('Cart/', Cart.as_view(), name='cart'),
      path('sign_up/',  views.sign_up , name='sign_up'),
      path('sign_up/sign_up/', views.sign_up, name='sign_up'),
      path('ul/', views.ul, name='ul'),
      path('ul/ul/', views.ul, name='ul'),
      path('user_profile/', views.user_profile, name='profile'),
      path('user_logout/', views.user_logout, name='user_logout'),
      path('about/', views.about, name='about'),
      path('test/', views.test, name='test'),
      path('check-out', Checkout.as_view() , name='checkout'),
      path('Orderview/', Orderview.as_view() , name='order'),


]