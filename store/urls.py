from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [

    # ---------------- PRODUCTS ----------------
    path('', views.product_list, name='product_list'),

    # ---------------- AUTH ----------------
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # ---------------- ORDERS ----------------
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='orders'),

    # ---------------- AI FEATURES ----------------

    # Smart search
    path('api/search/', views.smart_search, name='smart_search'),

    # Product recommendation
    path('api/recommend/<int:product_id>/', views.recommend_products, name='recommend_products'),

    # Price prediction
    path('api/predict-price/', views.predict_price, name='predict_price'),
    

]