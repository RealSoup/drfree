from django.shortcuts import render, redirect
from .models import Banner
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
import json

def is_admin_user(user):
    return user.is_active and user.is_staff

@user_passes_test(is_admin_user)

def index(request):
    context = {'banners': Banner.objects.all()}
    if request.method == 'POST':
        if request.FILES.get('image'):
            image = request.FILES['image']

            if not image:
                context['error'] = '이미지를 선택하세요.'
            elif not image.content_type.startswith('image/'):
                context['error'] = '이미지 파일만 업로드 가능합니다.'
            else:
                Banner.objects.create(
                    image  = image,
                    seq    = request.POST.get('seq', 0),  # 기본값 0
                    ip     = request.META.get('REMOTE_ADDR'),  # 요청한 클라이언트 IP
                    author 
                    = request.user  # 로그인한 유저
                )
                return redirect('adm.banner:index')
            
        elif 'order' in request.POST and request.POST['order'].strip():
            data = request.POST.get('order')
            if data:
                ids = json.loads(data)  # ['5', '3', '8', ...]
                for seq, pk in enumerate(ids):
                    Banner.objects.filter(pk=pk).update(seq=seq)
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'error'}, status=400)
        
        elif 'del' in request.POST and request.POST['del'].strip():
            pk = request.POST.get('del')
            Banner.objects.filter(pk=pk).delete()
            return JsonResponse({'status': 'ok'})

    return render(request, 'adm/banner/index.html', context)
