from django.contrib import admin
from django.urls import path, include
from main import views as main_view
urlpatterns = [
    path('',        main_view.index, name='main'),  # '/' 에 해당되는 path
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    path('common/', include('common.urls')),
    path('page/', include('page.urls')),
]
