from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

import uuid
import os



class StatusChoices(models.TextChoices):
    DISPLAY = "Display"
    NONE = "None"
        
class Notice(models.Model):
    bo_seq = models.IntegerField(default=0, null=False, blank=True)
    bo_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    bo_group = models.IntegerField(default=0, null=False, blank=True)
    bo_co_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bo_file = GenericRelation('BoFile', related_query_name='notice')
    summernote_images = GenericRelation('SummernoteImage', related_query_name='notice')
    bo_hit = models.IntegerField(default='0', null=False, blank=True)
    writer = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    pid = models.IntegerField(default=0, null=False, blank=True)
    def __str__(self):  # 관리자에 페이지에서 해당 모델표기가 오브제트가 아닌 제목으로 표시
        return self.subject
    
class Circle(models.Model):
    bo_seq = models.IntegerField(default=0, null=False, blank=True)
    bo_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    bo_group = models.IntegerField(default=0, null=False, blank=True)
    bo_co_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bo_file = GenericRelation('BoFile', related_query_name='circle')
    summernote_images = GenericRelation('SummernoteImage', related_query_name='circle')
    bo_hit = models.IntegerField(default='0', null=False, blank=True)
    writer = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    pid = models.IntegerField(default=0, null=False, blank=True)
    # def __str__(self):  # 관리자에 페이지에서 해당 모델표기가 오브제트가 아닌 제목으로 표시
    #     return self.subject    

class General(models.Model):
    bo_seq = models.IntegerField(default=0, null=False, blank=True)
    bo_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    bo_group = models.IntegerField(default=0, null=False, blank=True)
    bo_co_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bo_file = GenericRelation('BoFile', related_query_name='general')
    summernote_images = GenericRelation('SummernoteImage', related_query_name='general')
    bo_hit = models.IntegerField(default='0', null=False, blank=True)
    writer = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    pid = models.IntegerField(default=0, null=False, blank=True)
    def __str__(self):  # 관리자에 페이지에서 해당 모델표기가 오브제트가 아닌 제목으로 표시
        return self.subject

class Photo(models.Model):
    bo_seq = models.IntegerField(default=0, null=False, blank=True)
    bo_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    bo_group = models.IntegerField(default=0, null=False, blank=True)
    bo_co_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bo_file = GenericRelation('BoFile', related_query_name='photo')
    summernote_images = GenericRelation('SummernoteImage', related_query_name='photo')
    bo_hit = models.IntegerField(default='0', null=False, blank=True)
    writer = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    pid = models.IntegerField(default=0, null=False, blank=True)
    def __str__(self):  # 관리자에 페이지에서 해당 모델표기가 오브제트가 아닌 제목으로 표시
        return self.subject
    
class Video(models.Model):
    bo_seq = models.IntegerField(default=0, null=False, blank=True)
    bo_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    bo_group = models.IntegerField(default=0, null=False, blank=True)
    bo_co_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bo_file = GenericRelation('BoFile', related_query_name='video')
    summernote_images = GenericRelation('SummernoteImage', related_query_name='video')
    bo_hit = models.IntegerField(default='0', null=False, blank=True)
    writer = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    pid = models.IntegerField(default=0, null=False, blank=True)
    def __str__(self):  # 관리자에 페이지에서 해당 모델표기가 오브제트가 아닌 제목으로 표시
        return self.subject
    
class Story(models.Model):
    bo_seq = models.IntegerField(default=0, null=False, blank=True)
    bo_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    bo_group = models.IntegerField(default=0, null=False, blank=True)
    bo_co_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bo_file = GenericRelation('BoFile', related_query_name='story')
    summernote_images = GenericRelation('SummernoteImage', related_query_name='story')
    bo_hit = models.IntegerField(default='0', null=False, blank=True)
    writer = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    pid = models.IntegerField(default=0, null=False, blank=True)
    def __str__(self):  # 관리자에 페이지에서 해당 모델표기가 오브제트가 아닌 제목으로 표시
        return self.subject
    
class Build(models.Model):
    bo_seq = models.IntegerField(default=0, null=False, blank=True)
    bo_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    bo_group = models.IntegerField(default=0, null=False, blank=True)
    bo_co_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bo_file = GenericRelation('BoFile', related_query_name='build')
    summernote_images = GenericRelation('SummernoteImage', related_query_name='build')
    bo_hit = models.IntegerField(default='0', null=False, blank=True)
    writer = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    pid = models.IntegerField(default=0, null=False, blank=True)
    def __str__(self):  # 관리자에 페이지에서 해당 모델표기가 오브제트가 아닌 제목으로 표시
        return self.subject
    
class Other(models.Model):
    bo_seq = models.IntegerField(default=0, null=False, blank=True)
    bo_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    bo_group = models.IntegerField(default=0, null=False, blank=True)
    bo_co_seq_cd = models.CharField(max_length=10, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    bo_file = GenericRelation('BoFile', related_query_name='other')
    summernote_images = GenericRelation('SummernoteImage', related_query_name='other')
    bo_hit = models.IntegerField(default='0', null=False, blank=True)
    writer = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    pid = models.IntegerField(default=0, null=False, blank=True)
    def __str__(self):  # 관리자에 페이지에서 해당 모델표기가 오브제트가 아닌 제목으로 표시
        return self.subject    






# 공통 업로드 경로 생성 함수
def upload_to(filename, base_dir, bo_nm):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(base_dir, bo_nm, new_filename)

def summernote_upload_to(instance, filename):
    bo_nm = getattr(instance, 'bo_nm', None)
    bo_nm = bo_nm.lower() if bo_nm else 'etc'
    return upload_to(filename, 'summernote', bo_nm)

def bo_file_upload_to(instance, filename):
    bo_nm = instance.content_type.model if instance else 'etc'
    return upload_to(filename, 'board', bo_nm)

class SummernoteImage(models.Model):
    f_path = models.ImageField(upload_to=summernote_upload_to)
    bo_nm = models.CharField(max_length=50, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    bo = GenericForeignKey('content_type', 'object_id')  # 게시글 객체와 연결
    key = models.UUIDField(null=True, blank=True)  # 글 작성 중 유일키
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BoFile(models.Model):    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    f_path = models.FileField(upload_to=bo_file_upload_to)  # 서버 저장용 파일 (uuid 이름)
    origin_name = models.CharField(max_length=255, null=True, blank=True)        # 사용자 원본 파일명