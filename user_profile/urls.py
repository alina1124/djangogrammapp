from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>', views.profile, name='profile'),
    path('settings/edit', views.edit_profile, name='edit-profile'),
    path('follow/', views.follow, name='follow')
]