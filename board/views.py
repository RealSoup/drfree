from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone


from .forms import NoticeForm
from .models import Notice



def index(request, bo_nm):
    page = request.GET.get('page', '1')  # 페이지
    bo_list = Notice.objects.order_by('-create_date')
    paginator = Paginator(bo_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'bo_list': page_obj, 'bo_nm':bo_nm, 't':timezone.now()}
    return render(request, 'board/index.html', context)

def show(request, bo_nm, bo_id):
    bo = get_object_or_404(Notice, pk=bo_id)
    context = {'bo': bo, 'bo_nm':bo_nm}
    return render(request, 'board/show.html', context)




@login_required(login_url='common:login')
def create(req, bo_nm):
    if req.method == 'POST':
        form = NoticeForm(req.POST)
        if form.is_valid():
            bo = form.save(commit=False)
            bo.author = req.user  # author 속성에 로그인 계정 저장
            bo.create_date = timezone.now()
            bo.save()
            return redirect('board:index', bo_nm=bo_nm)
    else:
        form = NoticeForm()
    context = {'form': form}
    return render(req, 'board/form.html', context)

@login_required(login_url='common:login')
def edit(request, bo_nm, bo_id):
    bo = get_object_or_404(Question, pk=bo_id)
    if request.user != bo.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:show', bo_id=bo.id)
    if request.method == "POST":
        form = NoticeForm(request.POST, instance=bo)
        if form.is_valid():
            bo = form.save(commit=False)
            bo.modify_date = timezone.now()  # 수정일시 저장
            bo.save()
            return redirect('board:show', bo_id=bo.id)
    else:
        form = NoticeForm(instance=bo)
    context = {'form': form}
    return render(request, 'board/bo_form.html', context)

@login_required(login_url='common:login')
def delete(request, bo_nm, bo_id):
    bo = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:show', question_id=question.id)
    question.delete()
    return redirect('board:index')