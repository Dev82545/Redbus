from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name = 'redbus-home'),
    path('profile/', views.profile, name = 'profile' ),
    path('search/', views.search, name = 'search'),
    path('hlogin/', views.hlogin, name= 'hlogin'),
    path('hlogout/', views.hlogout, name= 'hlogout'),
    path('signup/', views.signup, name= 'signup'),
    
]
