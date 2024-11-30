from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # # path('', views.get_user),
    # # path('<int:pk>', views.GetUser.as_view())
    # path('<str:nickname>', views.GetUser.as_view()),
    # path('update/<int:pk>/', views.UpdatePostDescription.as_view()),
    # path('create/', views.CreatePost.as_view(), name='create_new_post'),
    # path("get_post/<int:pk>/", views.GetPost.as_view()),
    path('', views.MainView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)