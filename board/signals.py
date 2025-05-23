from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import os
from .models import SummernoteImage, BoFile

# 파일 데이터가 지워지면 실제 파일을 서버에서 지워라
@receiver(post_delete, sender=BoFile)
@receiver(post_delete, sender=SummernoteImage)
def delete_file_on_model_delete(sender, instance, **kwargs):
    file_field = getattr(instance, 'f_path', None)
    if file_field and hasattr(file_field, 'path') and os.path.isfile(file_field.path):
        try:
            os.remove(file_field.path)
        except Exception as e:
            print(f"파일 삭제 실패: {file_field.path} - {e}")