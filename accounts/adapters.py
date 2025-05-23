# accounts/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # 네이버에서 받은 이름 또는 닉네임을 username으로 지정
        extra_data = sociallogin.account.extra_data
        name = extra_data.get('name') or extra_data.get('nickname') or 'naveruser'
        
        # 중복 방지 처리
        base_username = name.strip().replace(" ", "")
        username = base_username
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        user.username = username
        return user
