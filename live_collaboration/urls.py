from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('matching/', views.matching, name='matching'),
]
