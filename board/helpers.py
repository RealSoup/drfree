# board/helpers.py

from .models import Notice

def get_new_bo_seq(model):
    """최저 bo_seq 값 구해서 다음 값을 반환"""
    m = model.objects.order_by('bo_seq').first()
    return (m.bo_seq-1) if m else -1

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
