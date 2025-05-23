from django.urls import path
from . import views

app_name = 'adm.banner'

urlpatterns = [
    path('', views.index, name='index'),
]