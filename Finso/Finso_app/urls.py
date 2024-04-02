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
    path('logout/', views.user_logout, name='logout'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('expenses/statistics/', views.expense_statistics, name='expense_statistics'),
    path('notifications/', views.notifications, name='notifications'),
    path('add_recurring_expense/', views.add_recurring_expense, name='add_recurring_expense'),
    
   
    
]