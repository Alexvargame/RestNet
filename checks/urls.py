

from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('',main_page,name='main_page_url'),
    path('checks/',ChecksListView.as_view(),name='checks_list_url'),
    #path('check_create/', CheckCreateView.as_view(),name='check_create_url'),
    path('check_create/', ChecksMultiCreateView.as_view(),name='check_create_url'),
    path('checks/<int:pk>/',CheckDetailView.as_view(),name='check_detail_url'),
    path('products/',ProductListView.as_view(),name='products_list_url'),
    path('products/<int:product_id>/',ProductDetailView.as_view(),name='product_detail_url'),
    path('products/create/',ProductCreateView.as_view(),name='product_create_url'),
    path('products/update/<int:product_id>/',ProductUpdateView.as_view(),name='product_update_url'),
    path('products/delete/<int:product_id>/',ProductDeleteView.as_view(),name='product_delete_url'),
    path('files/',FilesToRenderView.as_view(),name='files_to_render_url')

]
