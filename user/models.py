#user/models.py _저장되고 사용되는 데이터의 형태, 데이터베이스의 모델 (ORM)
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser): #auth 상속 받음
    class Meta:
        db_table = "my_user" #DB 이름 지정

    # 정보 종류=각 정보가 어떻게 저장되는지 지정 (상속 관계에 따라 auth_user에 있는 정보는 생략 가능)
    #username = models.CharField(max_length=20, null=False)
    #password = models.CharField(max_length=256, null=False)
    bio = models.CharField(max_length=256, default='')
    #created_at = models.DateTimeField(auto_now_add=True) #이 부분은 파이썬은 자동으로 생성되어서 어드민 계정에서 안보임
    #updated_at = models.DateTimeField(auto_now=True) #이 부분은 파이썬은 자동으로 생성되어서 어드민 계정에서 안보임
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')  # 장고 auth_user_model 과 n:m 관계