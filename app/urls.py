from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    path('', views.redirect_to_signin, name='home_redirect'),
    path('addtocart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('updatecart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('removefromcart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cartpageupdatecart/<int:product_id>/<str:action>/', views.cartpage_update_cart, name='cartpage_update_cart'),
    path('cartpageremovefromcart/<int:product_id>/', views.cartpage_remove_from_cart, name='cartpage_remove_from_cart'),
    path('signin/', views.signin, name='signin'),  
    path('register/', views.register, name='register'),  
    path('logout/', LogoutView.as_view(next_page='signin'), name='logout'), 
    path('cart/', views.cart, name='cart'),
    path('payment/', views.payment, name='payment'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),
    path('address/',views.address, name='address'),
]
