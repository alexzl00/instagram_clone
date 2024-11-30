from rest_framework import serializers
from api.models import User, Posts

import os
import dotenv
from supabase import create_client, Client
from PIL import Image

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

def get_supabase_client() -> Client:
    supabase_url = SUPABASE_URL
    supabase_key = SUPABASE_KEY
    return create_client(supabase_url, supabase_key)

def load_image_by_path(load_image_by_path):
    post_url = get_supabase_client().storage.from_('posts').get_public_url(load_image_by_path)
    return post_url

def get_image_type(image_path):
    try:
        with Image.open(image_path) as img:
            return img.format
    except IOError:
        return None

class PostsSerializer(serializers.ModelSerializer):
    # post_image_path = serializers.CharField(required=False, allow_blank=True)
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Posts
        # exclude = ['user']

        fields = '__all__'

# class PostSerialier(serializers.ModelSerializer):
#     post_image_path = serializers.CharField(required=False, allow_blank=True)
#     class Meta:
#         model = Posts
#         exclude = ['user']

class UpdatePostDescription(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ["post_description"]

class UserSerializer(serializers.ModelSerializer):
    posts = PostsSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'created_at',
            'nickname',
            'posts'
        ]
    
    def to_representation(self, instance):
        # Get the original representation (with posts as a list)
        representation = super().to_representation(instance)
        print(representation)

        # Convert the posts list to a dictionary with post_id as the key
        posts_list = representation.pop('posts', [])
        posts_dict = {post['id']: post for post in posts_list}

        representation['posts'] = posts_dict

        for value in representation['posts'].values():
            value['post_image_path'] = load_image_by_path(value['post_image_path'])

        # Add the transformed posts dictionary back to the representation

        return representation
    
    