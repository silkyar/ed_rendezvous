from django.urls import path

from . import views


urlpatterns = [
    path('', views.topics, name='topics'),
    path('<str:topic_name>/', views.preferences, name='preferences'),
    path('process_preferences/', views.process_preferences, name='process_preferences'),
]
