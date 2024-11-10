from django.shortcuts import render
from django.views import View
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import random
import string
from datetime import datetime

from PIL import Image

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from dataclasses import dataclass

from itertools import groupby
from operator import itemgetter

@dataclass
class User:
    id: int
    nickname: str
    name: str
    profile_image: str
    

comments = {

}


load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# supabase_client.py
def get_supabase_client() -> Client:
    supabase_url = SUPABASE_URL
    supabase_key = SUPABASE_KEY
    return create_client(supabase_url, supabase_key)



def get_comments_by_id(request):
    try:
        post_id = int(request.GET.get('id'))
        if not post_id:
            return JsonResponse({'error': 'ID parameter is required'}, status=400)
        try:
            return JsonResponse(comments[post_id], safe=False)
        except KeyError:
            data, count = get_supabase_client().from_('Comments').select('post_id, created_at, comment_text, id, User:user_id(nickname, name, profile_picture_path)').eq('post_id', post_id).execute()
            for i in range(0, len(data[1])):
                data[1][i]['User']['profile_picture_path'] = load_image_by_path(data[1][i]['User']['profile_picture_path'])
            
            # save the comments in running application
            comments[post_id] = data[1]
            return JsonResponse(data[1], safe=False)

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def insert_comment_by_id(request):
    try:
        if request.method == 'POST':
            post_id = int(request.POST.get('post_id'))

            # if the user inserts the comment before he cklicked to load all comments to that post
            # then we dont append the this comment to comments
            # because we will fetch this later from db, when the user clicks to load comments
            if post_id in comments:
                comments[post_id].append({'User': {'name': User.name, 'nickname': User.nickname, 'profile_picture_path': User.profile_image}, 'post_id': post_id, 'created_at': request.POST.get('post_time'), 'comment_likes': 0, 'comment_text': request.POST.get('comment')})
            return JsonResponse({'result': 'ok'})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)
        
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

@csrf_exempt
def get_logged_user(request) -> User:
    try:
        if request.method == 'POST':
            print(User.id)
            return JsonResponse({'result': {'User':{'id': User.id, 'name': User.name, 'nickname': User.nickname, 'profile_picture_path': User.profile_image}, 'created_at': datetime.now(), 'comment_likes': 0}})
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

    '''
        user = {
            post_image:...,
            post_description:...,
            nichname:...,
            hashtags:...,
        }
    '''

    # inserting new post to 'Posts' and saving post image to storage
    post_image = user['post_image']
    post_description = user['post_description']
    post_image_path = f'{user['nickname']}_post_image_{generate_random_string(10)}'
    get_supabase_client().storage.from_('posts').upload(file=post_image.read(), path=post_image_path, file_options={"content-type": f"image/{get_image_type(post_image)}"})
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


def group_hashtags_by_post(data) -> dict:
    post_hashtags = {}
    
    for item in data:
        post_id = item['post_id']
        hashtag = item['Hashtags']['hashtag_name']

        if post_id not in post_hashtags:
            post_hashtags[post_id] = []

        post_hashtags[post_id].append(hashtag)
    
    return post_hashtags

def load_post_hashtags():
    post_ids = [1, 2]
    data, count = get_supabase_client().from_('Post_hashtags').select('post_id, Hashtags(hashtag_name)').in_('post_id', post_ids).execute()
    sorted_hashtags = sorted(data[1], key=itemgetter('post_id'))
    return group_hashtags_by_post(sorted_hashtags)

def load_users_posts(users_posts: list[int]) -> dict[int: dict[str: dict, str: dict[int: dict]]]:
    # users_posts = ['User_1', 'User_2', 'User_3']
    # users_posts = [16, 17, 18]

    posts, count1 = get_supabase_client().table('Posts').select('id, post_image_path, created_at, post_description, user_id').in_('user_id', users_posts).execute()
    users, count2 = get_supabase_client().table('User').select('id, nickname, name, profile_picture_path)').in_('id', users_posts).execute()
    user_map = {user['id']: user for user in users[1]}

    # Group posts by user_id
    grouped_data = {}
    for post in posts[1]:
        user_id = post['user_id']
        
        # Ensure there's a list for this user ID
        if user_id not in grouped_data:
            grouped_data[user_id] = {
                'user': user_map.get(user_id),  # Get user details from the user_map
                'posts': {}
            }
        
        # Append the current post to the user's list of posts
        grouped_data[user_id]['posts'][int(post['id'])] = post

    posts_hashtags = load_post_hashtags()

    # grouped_data have the following structure:
    # {
    #     1: {
    #         'user': {
    #             'id': 1,
    #             'nickname': 'user1',
    #             'name': 'User One',
    #             'profile_picture_path': 'path/to/pic1.jpg'
    #         },
    #         'posts': {
    #             101: {
    #                 'id': 101,
    #                 'post_image_path': 'path/to/post1.jpg',
    #                 'created_at': '2024-10-22T10:00:00Z',
    #                 'post_description': 'A beautiful sunrise'
    #                 'post_hashtags': []
    #             }
    #         }
    #     }
    # }

    for user_id, value in grouped_data.items():
        value['user']['profile_picture_path'] = load_image_by_path(value['user']['profile_picture_path'])

        for post in value['posts'].values():
            post['post_image_path'] = load_image_by_path(post['post_image_path'])
            
            try:
                post['post_hashtags'] = posts_hashtags[post['id']]
            except KeyError:
                post['post_hashtags'] = []

    return grouped_data


def upload_file(request):
    if request.method == 'POST':
        post_image = request.FILES['file']
        post_description = request.POST.get('description')
        hashtags = request.POST.get('hashtags')
        
        '''
            user = {
                post_image:...,
                post_description:...,
                nickname:...,
                hashtags:...,
            }
        '''

        user = {
                'post_image': post_image,
                'post_description': post_description,
                'nickname': User.nickname,
                'hashtags': hashtags,
            }
        
        add_post_to_db(user, User.id)


        return render(request, 'main_view/main_html.html', {
            'user_profiles_list': load_users_recommendations(),
            'user_posts_list': load_users_posts([16, 17, 18]),
        })

class MainView(View):
    def get(self, request):

        load_user('User_1')
        
        # for user in user_posts_list:
        #     user_id = add_user_to_db(user)[1][0]['id']
        #     add_post_to_db(user, user_id)

        # add_post_to_db({'hashtags': '#hello #goodsupe #myname'}, 1)
        

        #load_users_posts()
        #load_post_hashtags()

        return render(request, 'main_view/main_html.html', {
            'user_profiles_list': load_users_recommendations(),
            'user_posts_list': load_users_posts([16, 17, 18]),
        })