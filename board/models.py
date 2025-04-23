from django.db import models
from django.contrib.auth.models import User

class StatusChoices(models.TextChoices):
    DISPLAY = "Display"
    NONE = "None"
        
class Notice(models.Model):    
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    display_top = models.CharField( max_length=7, choices=StatusChoices.choices, default=StatusChoices.DISPLAY, )
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)