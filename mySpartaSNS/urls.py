"""mySpartaSNS URL Configuration
*전체 API 담당 (맞는 URL-접속 경로를 찾아줌)*
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.base_response, name='first_test'), #views.py참고
    path('first/', views.first_view, name='first_view'), #views.py참고
    path('', include('user.urls')), # user앱의 urls.py에 연결시키겠다!
    path('', include('tweet.urls')),
]
