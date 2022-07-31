from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [

    path('',views.dashboard,name = 'dashboard'),
    path('add_budget',views.add_budget,name = 'add_budget'),
    path('edit_budget/<str:pk>',views.edit_budget,name = 'edit_budget'),
    path('delete_budget/<str:pk>',views.delete_budget,name = 'delete_budget'),
    path('add_actuals',views.add_actuals,name = 'add_actuals'),
    path('edit_actuals/<str:pk>',views.edit_actuals,name = 'edit_actuals'),
    path('delete_actuals/<str:pk>',views.delete_actuals,name = 'delete_actuals'),
    path('add_category',views.add_category,name = 'add_category'),
    path('monthly',views.monthly,name = 'monthly'),
    path('yearly',views.yearly,name = 'yearly'),
    path('category_manager',views.category_manager,name = 'category_manager'),
    path('edit_category/<str:pk>',views.edit_category,name = 'edit_category'),


    

    
]