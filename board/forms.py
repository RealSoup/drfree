from django import forms
from board.models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice  # 사용할 모델
        fields = ['subject', 'content'] 
        labels = {
            'subject': '제목',
            'content': '내용',
        }  
