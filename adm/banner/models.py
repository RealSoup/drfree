from django.db import models
from django.contrib.auth.models import User

class Banner(models.Model):
    image = models.ImageField(upload_to='adm/banner/')
    seq = models.IntegerField(default=0, null=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"메인 배너 ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        db_table = 'adm_banner'
        verbose_name = "메인 배너"
        verbose_name_plural = "메인 배너 목록"
        ordering = ['seq']