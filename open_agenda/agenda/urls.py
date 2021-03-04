from django.urls import path

from . import views

app_name = 'agenda'

urlpatterns = [
    path('',views.index, name='index'),
    path(r'update/',views.updateAgenda),
    path(r'get/', views.GetDate),
    path(r'weekly/', views.Weekly)
]