from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('my-orders/', views.order_history, name='order_history'),
    path('search/', views.smart_search, name='smart_search'),
    path('recommend/<int:product_id>/', views.recommend_products, name='recommend_products'),
    path('predict-price/', views.predict_price, name='predict_price'),
]