from django.shortcuts import render
from django.views import View
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

user_profiles_list = [
    {
        'nickname': 'why_not_donut',
        'name': 'Why Donut',
        'profile_picture': "static/main_view/images/why_not_donut_picture.jpg.avif"
    },
    {
        'nickname': "donuts_mother",
        'name': "Donut's Mother",
        'profile_picture': "static/main_view/images/donuts_mother.jpeg"
    }
]

comments = [
    {
        'post_id': 1,
        'nickname': 'Chubaka',
        'name': 'Chubaka First',
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'comment_likes': 123,
        'comment': 'Really funny init?'
    },
    {
        'post_id': 1,
        'nickname': 'Chubaka_new',
        'name': 'Chubaka First',
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'comment_likes': 12,
        'comment': 'good one'
    },
    {
        'post_id': 1,
        'nickname': 'Mother_Chubaka',
        'name': 'Chubaka First',
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'comment_likes': 1,
        'comment': 'Love you <3 Love you <3 Love you <3 Love you <3 Love you <3 Love you <3 Love you <3 Love you <3 Love you <3 Love you <3 Love you <3 Love you <3'
    },
    {
        'post_id': 1,
        'nickname': 'Chubaka',
        'name': 'Chubaka First',
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'comment_likes': 1234,
        'comment': 'love donut'
    },


    {
        'post_id': 2,
        'nickname': 'Chubaka',
        'name': 'Chubaka First',
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'comment_likes': 16,
        'comment': 'Oh man'
    },
    {
        'post_id': 2,
        'nickname': 'Chubaka_new',
        'name': 'Chubaka First',
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'comment_likes': 0,
        'comment': 'Juicy'
    },
    {
        'post_id': 2,
        'nickname': 'Mother_Chubaka',
        'name': 'Chubaka First',
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'comment_likes': 5,
        'comment': 'Love you donut Love you donut Love you donut Love you donut Love you donut <3 Love you <3 Love you <3 Love you <3'
    },
    {
        'post_id': 2,
        'nickname': 'Chubaka',
        'name': 'Chubaka First',
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'comment_likes': 76,
        'comment': 'love donut'
    },
]

def count_comments(id):
    response = 0
    for comment in comments:
        if comment['post_id'] == int(id):
            response += 1
    return response

user_posts_list = [
    {
        'id': 1,
        'nickname': 'User_1',
        'name': 'User First',
        'post_image': "static/main_view/images/post_image1.jpeg",
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'number_of_comments': count_comments(1),
        'post_description': 'This is post-description \nThis is post-description\nThis is post-description This is post-description This is post-description This is post-description This is post-description This is post-description'
    },
    {
        'id': 2,
        'nickname': 'User_2',
        'name': 'User Second',
        'post_image': "static/main_view/images/post_image2.webp",
        'profile_picture': "static/main_view/images/post_image2.webp",
        'post_time': '3 days ago',
        'number_of_comments': count_comments(2),
        'post_description': 'This is post-description \nThis is post-description'
    },
    {
        'id': 3,
        'nickname': 'User_3',
        'name': 'User Third',
        'post_image': "static/main_view/images/post_image3.jpeg",
        'profile_picture': "static/main_view/images/post_image3.jpeg",
        'post_time': '1 week ago',
        'number_of_comments': count_comments(3),
        'post_description': 'This is post-description \nThis is post-description\nThis is post-description This is post-description '
    }
]

load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# supabase_client.py
def get_supabase_client() -> Client:
    supabase_url = SUPABASE_URL
    supabase_key = SUPABASE_KEY
    return create_client(supabase_url, supabase_key)


def get_comments(id):
    response = []
    for comment in comments:
        if comment['post_id'] == int(id):
            response.append(comment)
    return response


def get_comments_by_id(request):
    try:
        post_id = request.GET.get('id')
        if not post_id:
            return JsonResponse({'error': 'ID parameter is required'}, status=400)

        return JsonResponse(get_comments(post_id), safe=False)

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def add_comment_to_db(request) -> None:
    post_id = request.POST.get('post_id')
    comment_text = request.POST.get('comment_text')
    data, count = get_supabase_client().table('Comments').insert({"post_id": post_id, 'comment_text': comment_text}).execute()
    
class MainView(View):
    def get(self, request):
        return render(request, 'main_view/main_html.html', {
            'user_profiles_list': user_profiles_list,
            'user_posts_list': user_posts_list,
            'comments': comments
        })