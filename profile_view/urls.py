from django.urls import path
from profile_view import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='user-profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)