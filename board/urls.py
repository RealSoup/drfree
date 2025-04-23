from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('<str:bo_nm>/',                    views.index, name='index'),
    path('<str:bo_nm>/<int:bo_id>/',        views.show, name='show'),

    path('<str:bo_nm>/create/',             views.create, name='create'),
    path('<str:bo_nm>/modify/<int:bo_id>/', views.edit, name='edit'),
    path('<str:bo_nm>/delete/<int:bo_id>/', views.delete, name='delete'),
]