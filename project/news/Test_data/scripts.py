from django.contrib.auth.models import User
from django.utils import timezone
from news.models import Author, Category, Post, Comment

# create users

user1 = User.objects.create_user("user1")
user2 = User.objects.create_user("user2")

# create authors

author1 = Author.objects.create(user_id=user1)
author2 = Author.objects.create(user_id=user2)

# create categories

category1 = Category.objects.create(name="Category 1")
category2 = Category.objects.create(name="Category 2")
category3 = Category.objects.create(name="Category 3")
category4 = Category.objects.create(name="Category 4")

# create post and news

post1 = Post.objects.create(author=author1, date=timezone.now(), heading="Post 1", text="Text1", raiting=1)
post2 = Post.objects.create(author=author2, date=timezone.now(), heading="Post 2", text="Text2", raiting=-1)
news1 = Post.objects.create(author=author1, date=timezone.now(), heading="News 1", text="News Text1", raiting=2, state="NE")

# assigning categories

post1.categories.add(category1, category3)
post2.categories.add(category2, category4)
news1.categories.add(category1, category4)

# create comments

comment1 = Comment.objects.create(user_id=user1, post=post1, text="I first))", comment_date=timezone.now())
comment1_1 = Comment.objects.create(user_id=user2, post=post1, text="And?", comment_date=timezone.now())
comment2 = Comment.objects.create(user_id=user2, post=post2, text="My first post))", comment_date=timezone.now())
comment2_1 = Comment.objects.create(user_id=user1, post=post2, text="well", comment_date=timezone.now())
comment3 = Comment.objects.create(user_id=user1, post=news1, text="I'm faster than you", comment_date=timezone.now())
comment3_1 = Comment.objects.create(user_id=user2, post=news1, text="Go touch the grass", comment_date=timezone.now())

# boring, but why i dont use ChatGPT?

post1.like()
post2.dislike()
news1.like()
comment1.like()
comment1_1.like()
comment2.like()
comment2_1.dislike()
comment3.dislike()
comment3_1.like()

# update user or author rating

author1.update_raiting()
author2.update_raiting()

# best user and his rating

best_user = Author.objects.all().order_by('-raiting').first()
print(f'Username: {best_user.user_id.username}, Rating: {best_user.raiting}')

# best post

best_post = Post.objects.all().order_by('-raiting').first()
print(f'Date: {best_post.date}, Author: {best_post.author.user_id.username}, Rating: {best_post.raiting}, '
      f'Heading: {best_post.heading}, Text Preview: {best_post.text[:50]}...')

# comments on best post

comments_to_best_post = Comment.objects.filter(post=best_post)
for comment in comments_to_best_post:
    print(f'Date: {comment.comment_date}, User: {comment.user_id.username}, Rating: {comment.comment_raiting}, Text: {comment.text}')