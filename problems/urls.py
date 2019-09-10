from django.urls import path

from . import views


urlpatterns = [
    path('problems/main', views.index, name='main'),
]
