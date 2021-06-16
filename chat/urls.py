from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('chat/', views.chat_view, name='chat'),
    path('logout/', views.logout, name='logout'),
]
