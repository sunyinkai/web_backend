from django.urls import path
from . import views
urlpatterns= [
    path('index/',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('post/<int:post_id>', views.post, name='post'),
    path('edit/<int:post_id>',views.edit,name='edit'),
    path('follow/<int:user_id>',views.follow),
    path('getFriendNews/',views.get_friend_news),
    path('newsOperate/',views.news_operate),
    path('commentOperate/',views.comment_operate),
    path('likeOperate/',views.like_operate),
]