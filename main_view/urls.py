from django.urls import path
from main_view import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.MainView.as_view()),

    # to fetch comments for the post to load
    path('get-comments/', views.get_comments_by_id, name='get_item_by_id'),
    path('insert-comment/', views.insert_comment_by_id),
    path('add-comment-to-db/', views.add_comment_to_db),
    path('get-logged-user/', views.get_logged_user),
    path('upload-file/', views.upload_file, name='upload_file')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)