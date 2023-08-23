from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_output, name='main_output'),
    path('index', views.index, name='index'),
    path('fetch_details',views.fetch_details,name='fetch_details'),
]
