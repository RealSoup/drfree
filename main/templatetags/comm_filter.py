from django import template
from board.models import Notice
from datetime import datetime

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def def_range(v1, v2=None, v3=None):
    if v2 == None:
        return range(v1)
    elif v3 == None:
        return range(v1, v2)
    else:
        return range(v1, v2, v3)
    

@register.filter()
def date_print(v, arg=None):
    if v in (None, ''):
        return ''
    else:
        rst=''
        now = datetime.now()
        
        if (now.year==v.year):
            if (now.strftime('%y-%m-%d') == v.strftime('%y-%m-%d')):
                rst = v.strftime('%H:%M')
            else:
                rst = v.strftime('%m-%d')
        else:
            rst = v.strftime('%y-%m-%d')
        return rst

@register.simple_tag(takes_context=True)
def img_h(context, v):
    if context['request'].user_agent.is_mobile:       
        v = 100
    return v
    
@register.inclusion_tag('board/index_mini.html', takes_context=True)
def bo_mini(context, bo_nm):
    user = context['request'].user
    bo_list = []
    if bo_nm == 'notice':
        bo_list = Notice.objects.order_by("-created_at")[:5]
    return {'bo_list': bo_list, 'user':user, 'bo_nm': bo_nm}