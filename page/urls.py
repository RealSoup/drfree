from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    path('p01/', views.p01, name='p01'),
    path('p02/', views.p02, name='p02'),
    path('p03/', views.p03, name='p03'),
    path('p04/', views.p04, name='p04'),
    path('p05/', views.p05, name='p05'),
    path('p06/', views.p06, name='p06'),
    path('p07/', views.p07, name='p07'),
]