from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),             # New Home Page
    path('shop/', views.index, name='index'),      # Shop All Page
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]