from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    user = request.user.is_authenticated  # 장고가 제공하는 사용자 모델을 사용 했을 때 쓸 수 있는 함수, 로그인 된 사용자 확인
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == "GET":
        user = request.user.is_authenticated  # 사용자가 로그인이 되어 있는지 확인하기

        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')  # TweetModel 에 저장된 모든 내용(모든 행) 불러옴(+최신 역순 정렬)
            return render(request, 'tweet/home.html', {'tweet': all_tweet})  # 딕셔너리를 tweet 이란 키로 저장 -> home.html 로 전달
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user  # 지금 로그인된 사용자 정보 담음
        content = request.POST.get('my-content', '')  # 글 작성이 되지 않았다면 빈칸으로
        tags = request.POST.get('tag', '').split(',')

        if content == '':  # 글이 빈칸이면 기존 tweet 과 에러를 같이 출력
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다'}, {'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            #my_tweet = TweetModel()
            #my_tweet.author = user  # 외래키로 연결
            #my_tweet.content = request.POST.get('my-content', '')  # 윗줄 하나가 해당 3줄 대체 가능
            for tag in tags:
                tag = tag.strip()  # tag 공백 제거
                if tag != '':
                    my_tweet.tags.add(tag)

            my_tweet.save()
            return redirect('/tweet')


@login_required()
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required()
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)  # 조건에 맞는 TweetModel 의 단일 행 저장
    all_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')  # 조건에 맞는 TweetComment 의 복수 행 저장

    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment': all_comment})
    # 저장된 내용(my_tweet, all_comment)을 각각 'tweet', 'comment' 라는 이름으로 tweet_detail.html 로 전달


@login_required()
def write_comment(request, id):
    if request.method == 'POST':
        current_tweet = TweetModel.objects.get(id=id)

        my_comment = TweetComment()  # 새로운 TweetComment 객체 생성
        my_comment.tweet = current_tweet  # 외래키로 연결
        my_comment.author = request.user  # 외래키로 연결
        my_comment.comment = request.POST.get('comment', '')  # 입력폼에서 POST 로 온 여러 데이터 중 comment 라는 이름의 데이터 받음, 없으면 공백
        my_comment.save()                                     # (tweet_detail.html 의 49번째 줄 참고)
        return redirect('/tweet/'+str(id))


@login_required()
def delete_comment(request, id):
    my_comment = TweetComment.objects.get(id=id)  # request id와 comment id가 같은 comment 모델에서 해당 단일 행을 my_comment 객체로 저장
    current_tweet_id = my_comment.tweet.id  # 현재 comment 의 트윗 창으로 이동하기 위해 해당 comment 의 tweet_id 저장

    my_comment.delete()
    return redirect('/tweet/'+str(current_tweet_id))


class TagCloudTV(TemplateView):  # 태그들을 모아놓는 태그클라우드를 만듦
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):  # 태그들을 모아서 화면에 전달하는 역할
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context