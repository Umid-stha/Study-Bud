from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('update_user/', views.updateUser, name='update-user'),

    path('', views.home, name='home'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('room/<str:pk>/', views.room, name='room'),

    path('create_room', views.create_room, name='create-room'),
    path('update_room/<str:pk>/', views.update_room, name='update-room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete-room'),

    path('delete_message/<str:pk>/', views.delete_message, name='delete-message'),
]