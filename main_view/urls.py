from django.urls import path
from main_view import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.MainView.as_view()),

    # to fetch comments for the post to load
    path('get-comments/', views.get_comments_by_id, name='get_item_by_id'),
    path('add-comment-to-db/', views.add_comment_to_db)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)