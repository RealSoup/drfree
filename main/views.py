from django.shortcuts import render, get_object_or_404
from adm.banner.models import Banner

def index(request):
    from django.urls import get_resolver

    for url_pattern in get_resolver().url_patterns:
        print(url_pattern)
        
    context = {'banners': Banner.objects.all()}
    return render(request, 'main.html', context)
