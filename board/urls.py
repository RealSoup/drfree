from django.urls import path, re_path, include
from . import views

app_name = 'board'

urlpatterns = [
    path('import-xe-docs/', views.import_xe_documents, name='import_xe_documents'),
    path('<str:bo_nm>/',                    views.index, name='index'),
    path('<str:bo_nm>/<int:bo_id>/',        views.show, name='show'),

    # path('<str:bo_nm>/create/',             views.create, name='create'),
    re_path(r'^(?P<bo_nm>\w+)/create(?:/(?P<bo_id>\d+))?/$', views.create, name='create'),
    path('<str:bo_nm>/edit/<int:bo_id>/',   views.edit, name='edit'),
    path('<str:bo_nm>/delete/<int:bo_id>/', views.delete, name='delete'),
    
    path('down/<int:file_id>',              views.download_file, name='file_down'),
    
    
    path('<str:bo_nm>/summernote_upload/', views.summernote_upload, name='summernote_upload'),
]