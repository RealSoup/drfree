# 실행시 수동으 지워짐        
# 관리 커맨드: 오래된 미사용 이미지 정리 (management/commands/cleanup_unused_summernote_images.py)
#   python manage.py cleanup_unused_summernote_images
class Command(BaseCommand):
    help = '오래된 미사용 Summernote 이미지를 삭제합니다.'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=2)
        unused_images = SummernoteImage.objects.filter(is_used=False, created_at__lt=cutoff)
        for img in unused_images:
            file_path = img.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
            img.delete()
        self.stdout.write(self.style.SUCCESS(f"{unused_images.count()}개의 Summernote 이미지를 삭제했습니다."))