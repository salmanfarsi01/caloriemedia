from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    content = models.TextField()
    # NEW: Add image field
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Post by {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_ai = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author_name}"
    
