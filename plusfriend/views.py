from os.path import basename
import requests
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, resolve_url
from django.utils import timezone
from .decorators import bot
from .models import Post


@bot
def on_init(request):
    return {'type': 'text'}


@bot
def on_message(request):
    user_key = request.JSON['user_key']
    type = request.JSON['type']        # text, photo, audio(m4a), video(mp4)
    content = request.JSON['content']  # photo 타입일 경우에는 이미지 URL

    if type == 'photo':
        img_url = content
        img_name = basename(img_url)
        res = requests.get(img_url, stream=True)
        post = Post(user=request.user)
        post.photo.save(img_name, ContentFile(res.content))
        post.save()
        response = '사진을 저장했습니다.'
    elif content == '!웹으로보고싶어':
        url = request.build_absolute_uri(resolve_url('plusfriend:post_list'))
        response = '''다음 주소로 접속해봐.
- 주소  : {}
- 아이디: {}
- 암호  : 네가 설정한 암호'''.format(url, request.user.username)
    elif content == '!잊어줘':
        Post.objects.filter(user=request.user).delete()
        response = '난 너에 대한 모든 것을 잊었어.'
    elif content.startswith('!내암호:'):
        password = content[5:].strip()
        request.user.set_password(password)
        request.user.save()
        response = '암호를 설정했어.'
    elif content.startswith('!보여줘:'):
        date = content[5:].strip()
        today = timezone.now().date()
        qs = Post.objects.filter(user=request.user)
        if date == '오늘':
            qs = qs.filter(
                created_at__year=today.year,
                created_at__month=today.month,
                created_at__day=today.day)
        elif date == '어제':
            yesterday = today - timedelta(days=1)
            qs = qs.filter(
                created_at__year=yesterday.year,
                created_at__month=yesterday.month,
                created_at__day=yesterday.day)

        response_list = []
        for idx, post in enumerate(qs.exclude(message=''), 1):
            response_list.append('[{}] {}'.format(idx, post.message))

        response_list.append('\n- 사진메세지는 제외했어.')
        response = '\n'.join(response_list)
    else:
        post = Post.objects.create(user=request.user, message=content)
        response = '포스팅을 저장했습니다.'

    return {
        'message': {
            'text': response,
        }
    }


@bot
def on_added(request):
    user_key = request.JSON['user_key']


@bot
def on_block(request, user_key):
    pass


@bot
def on_leave(request, user_key):
    pass


@login_required
def post_list(request):
    qs = Post.objects.filter(user=request.user)
    return render(request, 'plusfriend/post_list.html', {
        'post_list': qs,
    })