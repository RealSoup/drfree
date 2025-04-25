from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    path('p11/', views.p11, name='p11'),
    path('p12/', views.p12, name='p12'),
    path('p13/', views.p13, name='p13'),
    path('p14/', views.p14, name='p14'),
    path('p15/', views.p15, name='p15'),
    path('p16/', views.p16, name='p16'),
    path('p17/', views.p17, name='p17'),
    
    path('p21/', views.p21, name='p21'),
    path('p22/', views.p22, name='p22'),
    path('p23/', views.p23, name='p23'),
    
    path('p31/', views.p31, name='p31'),
    path('p32/', views.p32, name='p32'),
    path('p33/', views.p33, name='p33'),
]