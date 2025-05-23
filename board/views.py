from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, F, Func, IntegerField

from .forms import NoticeForm, CircleForm
from .models import Notice, Circle, General, Photo, Video, Story, Build, Other, BoFile, SummernoteImage
from django.apps import apps
from django.forms import modelform_factory
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden
from .constants import bo_info
import os
import uuid
import re
import board.helpers as hp
from django.db.models.functions import Length
from django.http import FileResponse

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.core.management.base import BaseCommand
from datetime import timedelta
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver



model_map = {
    'notice'    : Notice,
    'circle'    : Circle,
    'general'   : General,        
    'photo'     : Photo,    
    'video'     : Video,    
    'story'     : Story,    
    'build'     : Build,    
    'other'     : Other,    
}
ASCII_A = 65;  #	A의 아스키코드


def check_url(get_response):
    def wrapper(request, *args, **kwargs):
        global model_map
        match = re.match( r"^/board/([a-z]+)/$", request.path)
        if match:
            model = model_map.get(match.group(1))
            if not model:
                return HttpResponse("잘못된 모델 이름입니다.", status=400)
        return get_response(request, *args, **kwargs)
    return wrapper

@check_url
def index(request, bo_nm):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    
    # Model = apps.get_model('board', request.GET.get('modelName'))
    Model = apps.get_model('board', bo_nm)
    bo_list = Model.objects.filter(bo_co_seq_cd=None).order_by('bo_seq', 'bo_seq_cd', '-created_at')
    
    if kw:
        bo_list = bo_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw)  # 질문 글쓴이 검색
        ).distinct()
    paginator = Paginator(bo_list, 20)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'bo_list': page_obj, 'bo_nm':bo_nm, 'page': page, 'kw': kw, 'bo_info': bo_info[bo_nm]}
    return render(request, 'board/index.html', context)

@check_url
def show(request, bo_nm, bo_id):
    global model_map
    bo = get_object_or_404(model_map.get(bo_nm), pk=bo_id)
    co = model_map.get(bo_nm).objects.filter(bo_group=bo_id, bo_co_seq_cd__isnull=False).order_by('bo_co_seq_cd')
    
    # ContentType 가져오기
    bo_file_ContentType = ContentType.objects.get_for_model(bo)
    # 그 ContentType이 가리키는 모델 전체 데이터 가져오기
    bo_file = BoFile.objects.filter(content_type=bo_file_ContentType, object_id=bo_id)

    context = {'bo': bo, 'bo_nm':bo_nm, 'bo_file':bo_file, 'comment': co}
    return render(request, 'board/show.html', context)


def update_summernote_image(post, user, bo):
    used_paths = set(re.findall(r'/media/(summernote/\S+?\.(?:jpg|jpeg|png|gif|webp))', post['content'] or ''))
    ct = ContentType.objects.get_for_model(bo.__class__)

    images = SummernoteImage.objects.filter(
        Q(user=user, key=post['sn_key']) | Q(content_type=ct, object_id=bo.id)
    )
    print('이미지 처리')
    for img in images:
        file_path = img.f_path.name.replace('\\', '/')
        print(f'file_path :  {file_path}')
        print(f'used_paths : {used_paths}')
        if file_path in used_paths:
            img.key = None
            img.content_type = ct
            img.object_id = bo.id
            img.save()
        else:
            img.delete()
                    
@check_url
@login_required(login_url='common:login')
def create(req, bo_nm, bo_id=None):
    global model_map
    b_model = model_map.get(bo_nm)
    BoForm = modelform_factory(b_model, fields=["subject", "content"])

    if req.method == 'POST':
        post_data = req.POST.copy()
        
        if 'wri_type' in post_data and post_data['wri_type'] == 'comment':   #   댓글이라면
            post_data['subject'] = 'comment'
            
            
        form = BoForm(post_data)
        
        if form.is_valid():
            bo = form.save(commit=False)
            
            if 'wri_type' in post_data and post_data['wri_type'] == 'reply':
                papa = b_model.objects.get(pk=bo_id)
                papa_bo_seq_cd = papa.bo_seq_cd or ''
                
                sibling_cnt =  b_model.objects.filter(
                    bo_seq=papa.bo_seq,
                    bo_seq_cd__startswith=papa_bo_seq_cd,
                ).annotate(
                    bo_seq_cd_len=Length('bo_seq_cd')
                ).filter(
                    bo_seq_cd_len=len(papa_bo_seq_cd) + 1
                ).count()                
                
                bo.bo_seq = papa.bo_seq
                bo.bo_seq_cd = (papa_bo_seq_cd or '') + chr(ASCII_A+sibling_cnt)
      
            elif 'wri_type' in post_data and post_data['wri_type'] == 'comment':
                papa = b_model.objects.get(pk=bo_id)
                papa_bo_co_seq_cd = papa.bo_co_seq_cd or ''
         
                sibling_cnt =  b_model.objects.filter(
                    bo_seq=papa.bo_seq,
                    bo_co_seq_cd__startswith=papa_bo_co_seq_cd,
                ).annotate(
                    bo_co_seq_cd_len=Length('bo_co_seq_cd')
                ).filter(
                    bo_co_seq_cd_len=len(papa_bo_co_seq_cd) + 1
                ).count()                
                
                bo.bo_seq = papa.bo_seq
                bo.bo_group = papa.bo_group or papa.id
                bo.bo_co_seq_cd = (papa_bo_co_seq_cd or '') + chr(ASCII_A+sibling_cnt)
            else:
                bo.bo_seq = hp.get_new_bo_seq(b_model)

            bo.writer = req.user.username
            bo.ip = hp.get_client_ip(req)  # IP 주소 저장
            bo.author = req.user  # author 속성에 로그인 계정 저장
            bo.save()
      
            if not ('wri_type' in post_data and post_data['wri_type'] == 'comment'):   #   댓글이 아니라면
                update_summernote_image(post_data, req.user, bo)    #   게시판 에디터 이미지 사용 여부 업데이트
 
            # file upload
            for f in req.FILES.getlist("files"):
                up_f = BoFile(
                    content_type = ContentType.objects.get_for_model(b_model),
                    object_id = bo.id,
                    f_path = f,
                    origin_name=f.name
                )
                up_f.save()
            
        
            if 'wri_type' in post_data and post_data['wri_type'] == 'comment':
                url_id = papa.bo_group or bo_id
                return redirect('board:show', bo_nm=bo_nm, bo_id=url_id)
            else:
                return redirect('board:index', bo_nm=bo_nm)
    else:
        form = BoForm()
        sn_key = uuid.uuid4()
        if bo_id:            
            subject = b_model.objects.get(pk=bo_id).subject
            form.fields['subject'].initial = 'Re: '+subject
    context = {'form': form, 'bo_nm':bo_nm, 'bo_id': bo_id, 'bo_info': bo_info[bo_nm], 'sn_key': sn_key}
    return render(req, 'board/form.html', context)

@check_url
@login_required(login_url='common:login')
def edit(req, bo_nm, bo_id):
    global model_map
    bo = get_object_or_404(model_map.get(bo_nm), pk=bo_id)
    
    if req.user != bo.author:
        messages.error(req, '수정권한이 없습니다')
        return redirect('board:show', bo_id=bo.id)
    
    BoForm = modelform_factory(model_map.get(bo_nm), fields=["subject", "content"])
    if req.method == "POST":
        post_data = req.POST.copy()
        
        if 'wri_type' in post_data and post_data['wri_type'] == 'comment':   #   댓글이라면
            post_data['subject'] = 'comment'
            
        form = BoForm(post_data, instance=bo)
        if form.is_valid():
            bo = form.save(commit=False)
            bo.modify_date = timezone.now()  # 수정일시 저장
            bo.save()
            
            if not ('wri_type' in post_data and post_data['wri_type'] == 'comment'):   #   댓글이 아니라면
                update_summernote_image(post_data, req.user, bo)    #   게시판 에디터 이미지 사용 여부 업데이트
            
            # 파일 삭제 처리
            delete_file_ids = post_data.getlist('delete_files')
            for file_id in delete_file_ids:
                f = get_object_or_404(BoFile, id=file_id)
                # if os.path.isfile(f.f_path.path):
                #     os.remove(f.f_path.path)
                # 글삭제시에도 파일 삭제되기 위해 아래 시그널 사용
                f.delete()
            
            # file upload
            for f in req.FILES.getlist("files"):
                up_f = BoFile(
                    content_type = ContentType.objects.get_for_model(model_map.get(bo_nm)),
                    object_id = bo.id,
                    f_path = f,
                    origin_name=f.name
                )
                up_f.save()
       
            url_id = bo.bo_group or bo_id   #   댓글이거나 글쓰기거나
            return redirect('board:show', bo_nm=bo_nm, bo_id=url_id)
    else:
        form = BoForm(instance=bo)
        # ContentType 가져오기
        bo_file_ContentType = ContentType.objects.get_for_model(bo)
        # 그 ContentType이 가리키는 모델 전체 데이터 가져오기
        bo_file = BoFile.objects.filter(content_type=bo_file_ContentType, object_id=bo_id)
        sn_key = uuid.uuid4()
        
    context = {'form': form, 'sn_key': sn_key}
    
    if req.method == "GET":
        context['bo_file'] = bo_file
        context['bo_nm'] = bo_nm
    
    return render(req, 'board/form.html', context)

@check_url
@login_required(login_url='common:login')
def delete(req, bo_nm, bo_id):
    global model_map
    bo = get_object_or_404(model_map.get(bo_nm), pk=bo_id)

    if req.user.is_superuser or req.user == bo.author:
        bo.delete()
        if bo.bo_co_seq_cd is None:
            return redirect('board:index', bo_nm=bo_nm)
        else:
            return redirect('board:show', bo_nm=bo_nm, bo_id=bo.bo_group)
    else:
        messages.error(req, '삭제권한이 없습니다')
        return redirect('board:show', bo_nm=bo_nm, bo_id=bo.id)

def download_file(req, file_id):
    file = get_object_or_404(BoFile, id=file_id)  # FileModel: 실제 파일 저장된 모델
    file_path = file.f_path.path  # .path로 실제 경로 추출

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file.origin_name))
    else:
        raise Http404("File not found")

# 섬머 노트 (글쓰기 에디터)에서 글내용으로 이미지를 첨부하면 업로드 
@csrf_exempt  # 이미 CSRF 토큰을 헤더로 전달했기 때문에 괜찮음
def summernote_upload(request, bo_nm):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        uploaded = SummernoteImage.objects.create(
            f_path=image,
            user=request.user, 
            bo_nm=bo_nm, 
            key=request.POST.get('sn_key')
        )
        return JsonResponse({'url': uploaded.f_path.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)










import requests
import pymysql

from datetime import datetime
from pymysql.cursors import DictCursor

@csrf_exempt
def import_xe_documents(request):
    if request.method != 'GET':
        return HttpResponse('GET only', status=405)

    media_path_content = os.path.join('media', 'board', 'prev', 'content')
    media_path_attach = os.path.join('media', 'board', 'prev', 'attach')
    os.makedirs(media_path_content, exist_ok=True)
    os.makedirs(media_path_attach, exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ko,en-US;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://pre.drfreeschool.kr/'
    }

    old_conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='dr_old',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    new_conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='drfree',
        charset='utf8mb4',
        cursorclass=DictCursor
    )

    module_map = {
        160:    (3, 'board_circle',  '소모임'),
        156:    (1, 'board_notice',  '공지사항'),
        148:    (19, 'board_general',  '교육 및 일반자료'),
        150:    (21, 'board_photo',  '사진 자료'),
        152:    (23, 'board_video',  '영상 자료'),
        158:    (22, 'board_story',  '학교 이야기'),
        340541: (2, 'board_build',  '학사건축 이야기'),
        332047: (20, 'board_other',  '외부 게시판'),
    }

    with old_conn.cursor() as old_db, new_conn.cursor() as new_db:
        for module_srl, (content_type_id, table_name, menu_name) in module_map.items():
            print(f"\n=== [Importing {module_srl}번 메뉴: {menu_name}] ===")

            old_db.execute("""
                SELECT * FROM xe_documents 
                WHERE module_srl = %s AND status = 'PUBLIC'
                ORDER BY list_order DESC
            """, [module_srl])

            documents = old_db.fetchall()

            bo_seq = 0
            for idx, doc in enumerate(documents):
                # if idx < 58:
                #     continue
                # if idx == 59:
                #     break
                
                bo_seq -= 1
                subject = doc['title']
                content = doc['content']

                img_urls = re.findall(r'<img[^>]+src=\"([^\"]+)', content, re.IGNORECASE)
                replaced_urls = {}
                for img_url in img_urls:
                    if img_url.startswith('/'):
                        full_url = 'https://pre.drfreeschool.kr' + img_url
                    elif img_url.startswith('./'):
                        full_url = 'https://pre.drfreeschool.kr' + img_url[1:]
                    else:
                        full_url = img_url

                    filename = os.path.basename(full_url.split('?')[0])
                    content = content.replace(img_url, f'/media/board/prev/content/{filename}')
                    replaced_urls[full_url] = filename

                bo_hit = doc['readed_count']
                writer = doc['nick_name']
                created_at = datetime.strptime(doc['regdate'], '%Y%m%d%H%M%S')
                updated_at = datetime.strptime(doc['last_update'], '%Y%m%d%H%M%S')
                ip = doc['ipaddress']
                author_id = 1
                bo_group = doc.get('comment_count', 0)

                insert_sql = f"""
                    INSERT INTO {table_name}
                    (bo_seq, bo_seq_cd, bo_group, bo_co_seq_cd, subject, content, bo_hit,
                    writer, created_at, updated_at, ip, author_id, pid)
                    VALUES
                    (%s, NULL, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, 0)
                """
                new_db.execute(insert_sql, [
                    bo_seq, bo_group, subject, content, bo_hit,
                    writer, created_at, updated_at, ip, author_id
                ])
                new_conn.commit()

                new_db.execute("SELECT LAST_INSERT_ID() AS id")
                insert_id = new_db.fetchone()['id']

                for full_url, filename in replaced_urls.items():
                    local_path = os.path.join(media_path_content, filename)
                    try:
                        r = requests.get(full_url, headers=headers, timeout=10)
                        content_type = r.headers.get('Content-Type', '')
                        if r.status_code == 200 and 'image' in content_type:
                            with open(local_path, 'wb') as f:
                                f.write(r.content)
                            print(f"[✔ 저장됨] {filename} ({len(r.content)} bytes) / post_id={insert_id}")
                        else:
                            print(f"[⚠ 실패] {full_url} / status={r.status_code} / type={content_type} / post_id={insert_id} / original_id={doc['document_srl']}")
                    except Exception as e:
                        print(f"[오류] 이미지 다운로드 실패: {full_url} / {e} / post_id={insert_id} / original_id={doc['document_srl']}")

                if doc['comment_count']:
                    old_db.execute("""
                        SELECT * FROM xe_comments 
                        WHERE module_srl = %s AND document_srl = %s 
                        ORDER BY list_order DESC
                    """, [module_srl, doc['document_srl']])
                    comments = old_db.fetchall()

                    for k2, comment in enumerate(comments):
                        if comment['parent_srl']:
                            new_db.execute(f"SELECT * FROM {table_name} WHERE pid = %s", [comment['parent_srl']])
                            pa = new_db.fetchone()
                            if not pa:
                                continue
                            prefix_len = len(pa['bo_co_seq_cd'] or '')
                            new_db.execute(f"""
                                SELECT COUNT(*) AS cnt FROM {table_name}
                                WHERE bo_seq = %s
                                AND bo_co_seq_cd LIKE %s
                                AND CHAR_LENGTH(bo_co_seq_cd) = %s
                            """, [pa['bo_seq'], f"{pa['bo_co_seq_cd']}%", prefix_len + 1])
                            sibling_cnt = new_db.fetchone()['cnt']
                            bo_co_seq_cd = (pa['bo_co_seq_cd'] or '') + chr(65 + sibling_cnt)
                        else:
                            bo_co_seq_cd = chr(65 + k2)

                        comment_content = comment['content']
                        writer = comment['nick_name']
                        created_at = datetime.strptime(comment['regdate'], '%Y%m%d%H%M%S')
                        updated_at = datetime.strptime(comment['last_update'], '%Y%m%d%H%M%S')
                        ip = comment['ipaddress']

                        insert_comment_sql = f"""
                            INSERT INTO {table_name}
                            (bo_seq, bo_seq_cd, bo_group, bo_co_seq_cd, subject, content, bo_hit,
                            writer, created_at, updated_at, ip, author_id, pid)
                            VALUES
                            (%s, NULL, %s, %s, 'comment', %s, 0, %s, %s, %s, %s, 1, %s)
                        """
                        new_db.execute(insert_comment_sql, [
                            bo_seq, insert_id, bo_co_seq_cd, comment_content,
                            writer, created_at, updated_at, ip, comment['comment_srl']
                        ])

                old_db.execute("SELECT * FROM xe_files WHERE module_srl = %s AND upload_target_srl = %s", [module_srl, doc['document_srl']])
                attachments = old_db.fetchall()

                for file in attachments:
                    src_url = file['uploaded_filename']
                    if src_url.startswith('./'):
                        src_url = 'https://pre.drfreeschool.kr' + src_url[1:]

                    origin_name = file['source_filename'] or os.path.basename(src_url)
                    ext = os.path.splitext(origin_name)[1]
                    new_filename = str(uuid.uuid4()) + ext
                    local_path = os.path.join(media_path_attach, new_filename)

                    try:
                        r = requests.get(src_url, headers=headers, timeout=10)
                        if r.status_code == 200:
                            with open(local_path, 'wb') as f:
                                f.write(r.content)

                            new_db.execute("""
                                INSERT INTO board_bofile (content_type_id, object_id, f_path, origin_name)
                                VALUES (%s, %s, %s, %s)
                            """, [content_type_id, insert_id, f'board/prev/attach/{new_filename}', origin_name])
                        else:
                            print(f"[⚠ 첨부파일 실패] {src_url} / status={r.status_code} / post_id={insert_id} / original_id={doc['document_srl']}")
                    except Exception as e:
                        print(f"[첨부파일 오류] {src_url} / {e} / post_id={insert_id} / original_id={doc['document_srl']}")

        new_conn.commit()

    return HttpResponse('게시글 마이그레이션 완료')