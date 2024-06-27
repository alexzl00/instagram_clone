from django.shortcuts import render
from django.views import View
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import random
import string

from PIL import Image

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from dataclasses import dataclass

@dataclass
class User:
    id: int
    nickname: str
    name: str
    profile_image: str
    

user_profiles_list = [
    {
        'nickname': 'why_not_donut',
        'name': 'Why Donut',
        'profile_picture': "static/images/why_not_donut_picture.jpg.avif"
    },
    {
        'nickname': "donuts_mother",
        'name': "Donut's Mother",
        'profile_picture': "static/images/donuts_mother.jpeg"
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
        'post_image': "static/images/post_image1.jpeg",
        'profile_picture': "static/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'number_of_comments': count_comments(1),
        'post_description': 'This is post-description \nThis is post-description\nThis is post-description This is post-description This is post-description This is post-description This is post-description This is post-description'
    },
    {
        'id': 2,
        'nickname': 'User_2',
        'name': 'User Second',
        'post_image': "static/images/post_image2.webp",
        'profile_picture': "static/images/post_image2.webp",
        'post_time': '3 days ago',
        'number_of_comments': count_comments(2),
        'post_description': 'This is post-description \nThis is post-description'
    },
    {
        'id': 3,
        'nickname': 'User_3',
        'name': 'User Third',
        'post_image': "static/images/post_image3.jpeg",
        'profile_picture': "static/images/post_image3.jpeg",
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
    try:
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            comment_text = request.POST.get('comment_text')
            user_id = request.POST.get('user_id')
            data, count = get_supabase_client().table('Comments').insert({"post_id": post_id, 'comment_text': comment_text, 'user_id': user_id}).execute()
            if not post_id or not comment_text:
                raise ValueError("Missing post_id or comment_text")

            return JsonResponse({'result': 'ok'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_image_type(image_path):
    try:
        with Image.open(image_path) as img:
            return img.format
    except IOError:
        return None
    
def add_user_to_db(user):
    profile_picture = user['profile_picture']
    profile_picture_path = f'{user['nickname']}_profile_picture'
    get_supabase_client().storage.from_('posts').upload(file=profile_picture, path=profile_picture_path, file_options={"content-type": f"image/{get_image_type(profile_picture)}"})
    data, count = get_supabase_client().table('User').insert({'nickname': user['nickname'], 'name': user['name'], 'profile_picture_path': profile_picture_path}).execute()
    return data

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_post_to_db(user, user_id):

    # inserting new post to 'Posts' and saving post image to storage
    post_image = user['post_image']
    post_description = user['post_description']
    post_image_path = f'{user['nickname']}_post_image_{generate_random_string(10)}'
    get_supabase_client().storage.from_('posts').upload(file=post_image, path=post_image_path, file_options={"content-type": f"image/{get_image_type(post_image)}"})
    post_data, post_count = get_supabase_client().table('Posts').insert({'user_id': user_id, 'post_image_path': post_image_path, 'post_description': post_description}).execute()

    # inserting hashtags to new post
    if len(user['hashtags']) > 2:
        post_hashtags = ''.join(user['hashtags'][1:].split(' ')).split('#')
        hashtags_data, hashtags_count = get_supabase_client().table('Hashtags').select('*').in_('hashtag_name', post_hashtags).execute()
        
        for hashtag in hashtags_data[1]:
            # to sort out hashtags that are already in db, from that ones that are new
            post_hashtags.remove(hashtag['hashtag_name'])

        # check if some of hashtags that user typed in is new
        if len(post_hashtags) > 0:
            new_hashtags = [{'hashtag_name': hashtag} for hashtag in post_hashtags]

            new_inserted_hashtags, new_inserted_hashtags_count = get_supabase_client().table('Hashtags').insert(new_hashtags).execute()

            hashtags_to_post = [{'hashtag_id': id['id'], 'post_id': post_data[1][0]['id']} for id in new_inserted_hashtags[1]] + [{'hashtag_id': id['id'], 'post_id': post_data[1][0]['id']} for id in hashtags_data[1]]
        else:
            hashtags_to_post = [{'hashtag_id': id['id'], 'post_id': post_data[1][0]['id']} for id in hashtags_data[1]]

        data, count = get_supabase_client().table('Post_hashtags').insert(hashtags_to_post).execute()


def load_image_by_path(load_image_by_path):
    post_url = get_supabase_client().storage.from_('posts').get_public_url(load_image_by_path)
    print(post_url)
    return post_url

def load_user(nickname):
    data, count = get_supabase_client().table('User').select('*').eq('nickname', nickname).execute()
    User.id = data[1][0]['id']
    User.nickname = nickname
    User.name = data[1][0]['name']

    # get image from storage by path
    User.profile_image = load_image_by_path(data[1][0]['profile_picture_path'])

def load_users_recommendations():
    users_to_recommend = ['why_not_donut', 'donuts_mother']
    data, count = get_supabase_client().table('User').select('*').in_('nickname', users_to_recommend).execute()

    # get image from storage by path
    for i in range(0, len(data[1])):
        # swipe path to image in storage with an http link to our image
        data[1][i]['profile_picture_path'] = load_image_by_path(data[1][i]['profile_picture_path'])
    return data[1]

def load_users_posts():
    users_posts = ['User_1', 'User_2', 'User_3']
    data, count = get_supabase_client().table('User').select('id, nickname, name, profile_picture_path, Posts!Posts_user_id_fkey(id, post_image_path, created_at, post_description)').in_('nickname', users_posts).execute()
    
    # get image from storage by path
    for i in range(0, len(data[1])):
        # swipe path to image in storage with an http link to our image
        data[1][i]['profile_picture_path'] = load_image_by_path(data[1][i]['profile_picture_path'])
        data[1][i]['Posts'][0]['post_image_path'] = load_image_by_path(data[1][i]['Posts'][0]['post_image_path'])
    print(data[1])
    return data[1]

class MainView(View):
    def get(self, request):
        
        # for user in user_posts_list:
        #     user_id = add_user_to_db(user)[1][0]['id']
        #     add_post_to_db(user, user_id)

        # add_post_to_db({'hashtags': '#hello #goodsupe #myname'}, 1)
        

        #load_users_posts()

        return render(request, 'main_view/main_html.html', {
            'user_profiles_list': load_users_recommendations(),
            'user_posts_list': user_posts_list,
            'comments': comments
        })