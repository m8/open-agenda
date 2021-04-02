from django.urls import path

from . import views

app_name = 'agenda'

urlpatterns = [
    path('',views.index, name='index'),
    path(r'update/',views.updateAgenda),
    path(r'get/', views.GetDate),
    path(r'weekly/', views.Weekly),
    path(r'calendar/', views.Calendar),
    path(r'add-project/',views.AddProject),
    path(r'delete/',views.Delete),
    path(r'settings/',views.Settings),
    path(r'download-notes/',views.DownloadNotes),
    path(r'getEvents/',views.CalendarSource)
]