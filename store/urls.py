from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('signup/', views.signup, name='signup'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='orders'),
]