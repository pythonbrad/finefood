from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='home'),
    path('search/', views.restaurants_list, name='restaurants_list'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/signin/', views.signin, name='signin'),
    path('accounts/logout/', views.logout, name='logout'),
    path('<code>', views.restaurant_page, name='restaurant_page'),
]
