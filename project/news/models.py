from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse

post = "PO"
news = "NE"

STATE = [
    (post, "Post"),
    (news, "News")
]


class Author(models.Model):
    raiting = models.FloatField(default=0)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    subcribes = models.ManyToManyField(User, blank=True, related_name="author")

    def __str__(self):
        return f"{self.user_id.username}"

    def update_raiting(self):
        post_raiting = sum(post.raiting * 3 for post in Post.objects.filter(author=self))
        comments_raiting = sum(comment.comment_raiting for comment in Comment.objects.filter(user_id=self.user_id))
        self.raiting = post_raiting + comments_raiting
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=155)
    subcribes = models.ManyToManyField(User, blank=True, related_name="category")

    def __str__(self):
        return f'{self.name.title()}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    state = models.CharField(max_length=2, choices=STATE, default=post)
    date = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=155)
    text = models.TextField()
    raiting = models.FloatField(default=0)
    categories = models.ManyToManyField(Category, through="PostCategory")

    def like(self):
        self.raiting += 1
        self.save()

    def dislike(self):
        self.raiting -= 1
        self.save()

    def __str__(self):
        return f" {self.heading} by {self.author.user_id}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_raiting = models.FloatField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def like(self):
        self.comment_raiting += 1
        self.save()

    def dislike(self):
        self.comment_raiting -= 1
        self.save()

    def __str__(self):
        return self.text


class InterestingPost(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_heading = models.CharField(max_length=155)
    post_date = models.DateTimeField()

    def fill_details_of_post(self):
        self.post_date = self.post_id.date
        self.post_heading = self.post_id.heading


class InterestingPosts(models.Model):
    news = models.ForeignKey(InterestingPost, on_delete=models.CASCADE)
