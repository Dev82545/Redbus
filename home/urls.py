from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name = 'redbus-home'),
    path('profile/', views.profile, name = 'profile'),
    path('accounts/login/', views.hlogin, name = 'alogin'),
    path('search/', views.search, name = 'search'),
    path('login/', views.hlogin, name= 'login'),
    path('hlogout/', views.hlogout, name= 'hlogout'),
    path('signup/', views.signup, name= 'signup'),
    path('wallet/',views.wallet_topup, name = 'wallet'),
    path('cancel/<int:booking_id>/', views.cancel, name='cancel_booking')
]
