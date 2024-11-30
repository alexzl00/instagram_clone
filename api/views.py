from django.shortcuts import render
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.renderers import TemplateHTMLRenderer

# Create your views here.
from api.serializer import UserSerializer, UpdatePostDescription, PostsSerializer
from api.models import User, Posts, Post_hashtags, Hashtags
from api.serializer import get_supabase_client

from main_view.views import generate_random_string, get_image_type, load_image_by_path

def get_post_hashtags(post_id):
    
    data = Hashtags.objects.filter(post_hashtags__post_id=post_id).values('hashtag_name')
    return [hashtag['hashtag_name'] for hashtag in data]

class MainView(generics.ListAPIView, ListModelMixin):
    serializer_class = UserSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_view/main_html.html'

    def get_queryset(self):
        response = User.objects.filter(nickname__in=['User_1', 'User_2']).prefetch_related(
            Prefetch('posts', queryset=Posts.objects.all())
        )
        data = {}
        for user in response:
            user_data = model_to_dict(user)
            user_data['profile_picture_path'] = load_image_by_path(user_data['profile_picture_path'])

            posts = {}
            for post in user.posts.all().values():
                post['post_image_path'] = load_image_by_path(post['post_image_path'])
                post['hashtags'] = get_post_hashtags(post['id'])
                posts[post['id']] = post

            data[user_data['id']] = {
                'user': user_data,
                'posts': posts
            }
        print(data)
        return data

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(data={'user_posts_list': queryset}, template_name=self.template_name)

@api_view(['GET'])
def get_user(request, *args, **kwargs):
    instance = UserSerializer(data=request.data)
    if instance.is_valid():
        return Response(instance.data)
    return Response(request.data)

class GetUser(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'nickname'

    def get_queryset(self):
        return User.objects.all()

class GetPost(generics.RetrieveAPIView):
    serializer_class = PostsSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Posts.objects.all()


class RetrieveUser(generics.RetrieveAPIView):

    serializer_class = UserSerializer
    lookup_field = 'nickname'

    def get_queryset(self):
        return User.objects.all()
    
class UpdatePostDescription(generics.UpdateAPIView):
    serializer_class = UpdatePostDescription
    lookup_field = "pk"

    def get_queryset(self):
        return Posts.objects.all()
    
    def perform_update(self, serializer):
        print(serializer)
        # Custom update logic (if any)
        return super().perform_update(serializer)
    
class CreatePost(generics.CreateAPIView, CreateModelMixin):
    serializer_class = PostsSerializer
    queryset = Posts.objects.all()

    def create(self, request, *args, **kwargs):
        post_image_path = f'User_1_post_image_{generate_random_string(10)}'
        post_image = self.request.FILES.get('file')
        get_supabase_client().storage.from_('posts').upload(file=post_image.read(), path=post_image_path, file_options={"content-type": f"image/{get_image_type(post_image)}"})

        post_data = {
            'user': 16,
            'post_image_path': post_image_path,
            "post_description": self.request.POST.get('description')
        }
        serializer = self.get_serializer(data=post_data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)