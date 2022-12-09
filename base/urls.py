from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create-post'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete-post/', views.delete_post, name='delete-post'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('posts/<uuid:post_id>', views.post_view, name='post-view'),
    path('like-post', views.like_post, name='like-post'),
    path('tags/<str:tag_name>', views.tag_view, name='tags'),
    path('explore', views.explore, name='explore'),
    path('search', views.search, name='search'),
    path('comment/<str:post_id>', views.comment, name='comment'),
    path('like-comment', views.like_comment, name='like-comment'),
    path('reply/<int:comment_id>', views.reply, name='reply')
]
