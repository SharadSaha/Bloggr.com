from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('About/',views.about,name='About'),
    path('Contact/',views.contact,name='Contact'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'),
    path('addpost/',views.add_post,name='addpost'),
    path('updatepost/<int:id>/',views.update_post,name='updatepost'),
    path('deletepost/<int:id>/',views.delete_post,name='deletepost'),
]
