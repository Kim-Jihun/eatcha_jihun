from django.shortcuts import render
from .decorators import bot
from . import functions
from shop.models import Post, Tag, Rating
from django.http import JsonResponse

@bot
def on_init(request):

    return {'type': 'buttons', 'buttons': ['서울대입구', '신촌', '왕십리', '왜 안되나 아무거나 시험']}
    #return {'type': 'text'}


@bot
def on_message(request):

    user_key = request.JSON['user_key']
    type = request.JSON['type']
    content = request.JSON['content'] # photo 타입일 경우에는 이미지 URL



    if '서울대' in content:
        qs = Post.objects.filter(tag_set__location__icontains='서울대')
        ordered_query = qs.order_by('-score')
        response = ordered_query[0]
    elif '신' in content:
        qs = Post.objects.filter(tag_set__location__icontains='신촌')
        ordered_query = qs.order_by('-score')
        response = ordered_query[0]

    elif '왕십리' in content:

        qs = Post.objects.filter(tag_set__location__icontains='왕십리')
        ordered_query = qs.order_by('-score')
        response = ordered_query[0]

    else:
        response='지원하는 답변이 아닙니다.'


    if isinstance(response, str):

        return {
            'message': {
                'text': user_key + type + content
            }
        }
    else:
        return {
            'message': {
                'text': '식당이름:' + response.title,
                'photo': {
			#"url": 'https://s3.ap-northeast-2.amazonaws.com/eatcha' + response.image.url,
            "url": 'https://s3.ap-northeast-2.amazonaws.com/eatcha/media/srchttp3A2F2Fblogfiles.naver.net2F20150529_1362Fwdojo_1432876822368n6oMb_JPEG2FIMG_7019.JPG',
			"width": 640,
			"height": 480,
		},
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
