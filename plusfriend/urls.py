from django.urls import path, re_path
from . import views

app_name = 'plusfriend'

urlpatterns = [
    path('keyboard', views.on_init),
    path('friend', views.on_added),
    re_path(r'^friend/(?P<user_key>[\w-]+)$', views.on_block),
    re_path(r'^chat_room/(?P<user_key>[\w-]+)$', views.on_leave),
    path('message', views.on_message),
    path('diary/', views.post_list, name='post_list'),
]