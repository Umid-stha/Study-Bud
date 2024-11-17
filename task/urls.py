from . import views
from django.urls import path

urlpatterns=[
    path('', views.taskManager, name='tasks'),
    path('completed/<int:pk>/', views.completed, name='complete'),
    path('delete/<int:pk>/', views.delete, name='delete')

]