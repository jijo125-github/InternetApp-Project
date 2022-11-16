from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'about/', views.about, name='about'),
    path(r'<int:cat_no>/', views.detail, name='detail'),
    path(r'products/', views.products, name='products'),
    path(r'place_order/', views.place_order, name='placeOrder'),
    path(r'products/<int:prod_id>/', views.productdetail, name='productDetail'),
    path(r'orders/', views.myorders, name='orders')
]
