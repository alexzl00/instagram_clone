import os
from django.shortcuts import render
from django.views import View
from dotenv import load_dotenv
from supabase import create_client, Client
from main_view.views import User, load_users_posts, load_user

# Create your views here.
load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# supabase_client.py
def get_supabase_client() -> Client:
    supabase_url = SUPABASE_URL
    supabase_key = SUPABASE_KEY
    return create_client(supabase_url, supabase_key)

user_posts = [
    # {
    #     'img': 'static/images/donut_profile_picture.jpeg'
    # },
    # {
    #     'img': 'static/images/donuts_mother.jpeg'
    # },
    # {
    #     'img': 'static/images/post_image1.jpeg'
    # },
    # {
    #     'img': 'static/images/post_image3.jpeg'
    # } 
]


class ProfileView(View):
    def get(self, request):
        load_user('User_1')
        user_posts = load_users_posts([User.id])
        for i in user_posts.values():
            for y in i['posts'].values():
                print(y['post_image_path'])
        return render(request, 'profile_view/profile.html', {
            'user_posts': user_posts
        })