from django.contrib import admin #장고에서 admin 툴을 사용하겠다!
from .models import UserModel #현 위치의 모델에서 생성한 모델(UserModel)을 가져오겠다! (models.py의 클래스 이름)

# Register your models here.
admin.site.register(UserModel) # 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다 (127.0.0.1/admin에 접속해보자!)