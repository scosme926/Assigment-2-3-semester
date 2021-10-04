from django.urls import path
from . import views


urlpatterns = [
    path('api/version', views.version_endpoint, name='version_endpoint'),
    path('api/hello', views.hello_endpoint, name='hello_endpoint'),
    path('api/sellers', views.list_create_seller_endpoint, name="list_create_seller_endpoint"),
    path('api/seller/<id>', views.detail_update_delete_seller_endpoint, name='detail_update_delete_seller_endpoint'),
    path('api/products', views.list_create_product_endpoint, name='list_create_product_endpoint'),
    path('api/product/<id>', views.detail_update_delete_product_endpoint, name='detail_update_delete_product_endpoint'),
]
