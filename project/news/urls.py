from django.urls import path
# Импортируем созданные нами представления
from .views import PostsList, PostDetails, PostCreate, PostDelete, PostUpdate, subscribe_category, subscribe_author, \
   CommentCreate

urlpatterns = [

   path('', PostsList.as_view(),name="post_list"),
   path('<int:pk>', PostDetails.as_view(), name="post_detail" ),
   path('create/', PostCreate.as_view(), name="post_create"),
   path('news/create/', PostCreate.as_view(), name="news_create"),
   path('<int:pk>/update/', PostUpdate.as_view(), name="post_update"),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name="post_update"),
   path('<int:pk>/delete/', PostDelete.as_view(), name="post_delete"),
   path('news/<int:pk>/update/', PostDelete.as_view(), name="news_delete"),
   path('<int:post_id>/category/<int:category_id>/subscribe', subscribe_category, name='subscribe'),
   path('<int:post_id>/author/<int:author_id>/subscribe', subscribe_author, name='subscribe'),
   path('<int:post_id>/comment', CommentCreate.as_view(), name="comment_add")

]