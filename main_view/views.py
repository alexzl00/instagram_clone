from django.shortcuts import render
from django.views import View
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from django.conf import settings

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

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


user_posts_list = [
    {
        'nickname': 'User_1',
        'name': 'User First',
        'post_image': "static/main_view/images/post_image1.jpeg",
        'profile_picture': "static/main_view/images/post_image1.jpeg",
        'post_time': '1 day ago',
        'post_description': 'This is post-description \nThis is post-description\nThis is post-description This is post-description This is post-description This is post-description This is post-description This is post-description'
    },
    {
        'nickname': 'User_2',
        'name': 'User Second',
        'post_image': "static/main_view/images/post_image2.webp",
        'profile_picture': "static/main_view/images/post_image2.webp",
        'post_time': '3 days ago',
        'post_description': 'This is post-description \nThis is post-description'
    },
    {
        'nickname': 'User_3',
        'name': 'User Third',
        'post_image': "static/main_view/images/post_image3.jpeg",
        'profile_picture': "static/main_view/images/post_image3.jpeg",
        'post_time': '1 week ago',
        'post_description': 'This is post-description \nThis is post-description\nThis is post-description This is post-description '
    }
]

# supabase_client.py
def get_supabase_client() -> Client:
    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_KEY
    return create_client(supabase_url, supabase_key)




class MainView(View):
    def get(self, request):
        return render(request, 'main_view/main_html.html', {
            'user_profiles_list': user_profiles_list,
            'user_posts_list': user_posts_list
        })