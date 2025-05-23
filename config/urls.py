from django.contrib import admin
from django.urls import path, include
from main import views as main_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',        main_view.index, name='main'),  # '/' 에 해당되는 path
    path('board/', include('board.urls')),
    path('common/', include('common.urls')),
    path('page/', include('page.urls')),
    
    path('accounts/', include('allauth.urls')),  # allauth의 모든 URL 포함
    
    
    path('admin', admin.site.urls),  # 기본 어드민
        
    path('adm/', include([
        path('banner/', include('adm.banner.urls')),  # 커스텀 관리자
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)