#실질적으로 프로그램이 동작하는 부분, url을 요청하고 응답하는 그 사이에 일어나는 '서비스'들이 존재하는 곳
from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')

    elif request.method == 'POST':  # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get('username', '') #POST로 온 여러 데이터 중 username이름(name속성)의 데이터(없다면 ''처리)를 username 변수에 저장
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2: #비밀번호 안 맞으면 다시 작성하라고 페이지 다시 띄움
            return render(request, 'user/signup.html', {'error':'패스워드를 확인 해 주세요'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 입니다'})
            #exist_user = UserModel.objects.filter(username=username)
            exist_user = get_user_model().objects.filter(username=username) #동일 아이디 있는지 확인
            if exist_user:
                return render(request, 'user/signup.html', {'error':'사용자가 존재합니다'})
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 기존의 유저가 있는지 확인
        me = auth.authenticate(request, username=username, password=password) #사용자 정보를 장고가 알아서 가져와 줌(기본 기능)
        #me = UserModel.objects.get(username=username)  #UserModel에서 username값과 Post의 username이 같은 객체를 불러와 me에 저장

        if me is not None:  # 사용자가 있으면
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'유저 이름 혹은 패스워드를 확인 해 주세요'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required  # 로그인 한 사용자만 접근 할 수 있게 해 주는 기능
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude 와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user  # 로그인한 사용자 정보 me로 받음
    click_user = UserModel.objects.get(id=id)  # 팔로우 하거나 언팔할 사용자 정보

    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)

    return redirect('/user')