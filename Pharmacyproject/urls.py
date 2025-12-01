"""Pharmacyproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pharmacyapp.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('admin_login/', admin_login, name="admin_login"),
    path('pharmacist_login/', pharmacist_login, name="pharmacist_login"),
    path('dashboard/', dashboard, name="dashboard"),
    path('user_dashboard/', user_dashboard, name="user_dashboard"),
    path('user_inventory/', user_inventory, name="user_inventory"),
    path('admin_medicine_inventory/', admin_medicine_inventory, name="admin_medicine_inventory"),
    path('logout_admin/', logout_admin, name="logout_admin"),
    path('logout_user/', logout_user, name="logout_user"),
    path('admin_change_password/', admin_change_password, name="admin_change_password"),
    path('user_change_password/', user_change_password, name="user_change_password"),
    path('user_profile/', user_profile, name="user_profile"),
    path('user_search_medicine/', user_search_medicine, name="user_search_medicine"),
    path('user_cart/', user_cart, name="user_cart"),
    path('user_invoice/', user_invoice, name="user_invoice"),
    path('admin_invoice/', admin_invoice, name="admin_invoice"),
    path('admin_stock_report/', admin_stock_report, name="admin_stock_report"),
    path('admin_sales_report/', admin_sales_report, name="admin_sales_report"),
    path('admin_pharmacist_report/', admin_pharmacist_report, name="admin_pharmacist_report"),
    path('add_company/', add_company, name="add_company"),
    path('edit_company/<int:pid>/', add_company, name="edit_company"),
    path('view_company/', view_company, name="view_company"),
    path('delete_company/<int:pid>/', delete_company, name="delete_company"),
    path('add_medicine/', add_medicine, name="add_medicine"),
    path('edit_medicine/<int:pid>/', add_medicine, name="edit_medicine"),
    path('view_medicine/', view_medicine, name="view_medicine"),
    path('delete_medicine/<int:pid>/', delete_medicine, name="delete_medicine"),
    path('add_pharmacist/', add_pharmacist, name="add_pharmacist"),
    path('edit_pharmacist/<int:pid>/', add_pharmacist, name="edit_pharmacist"),
    path('view_pharmacist/', view_pharmacist, name="view_pharmacist"),
    path('delete_pharmacist/<int:pid>/', delete_pharmacist, name="delete_pharmacist"),
    path('add-cart/<int:pid>/', add_cart, name="add_cart"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),
    path('user_sales_report/', user_sales_report, name="user_sales_report"),
    path('delete_order/<int:pid>/', delete_order, name="delete_order"),
    path('user_delete_order/<int:pid>/', user_delete_order, name="user_delete_order"),
    path('order/', order, name="order"),
    path('user_order/', user_order, name="user_order"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
