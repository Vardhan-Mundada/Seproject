from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('register/', views.register, name='register'),
     path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),



]