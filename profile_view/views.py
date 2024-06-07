from django.shortcuts import render
from django.views import View

# Create your views here.

user_posts = [
    {
        'img': 'static/images/donut_profile_picture.jpeg'
    },
    {
        'img': 'static/images/donuts_mother.jpeg'
    },
    {
        'img': 'static/images/post_image1.jpeg'
    },
    {
        'img': 'static/images/post_image3.jpeg'
    } 
]

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile_view/profile.html', {
            'user_posts': user_posts
        })