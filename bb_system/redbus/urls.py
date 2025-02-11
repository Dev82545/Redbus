from django.urls import path
from . import views
urlpatterns = [
    path('',views.redbus,name = 'redbus'),
    path('<str:slug>/', views.red, name = 'red'),
    path('<str:slug>/seat/',views.seat, name = 'seat')
]
