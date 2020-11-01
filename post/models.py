from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
User=get_user_model()
# Create your models here.
class Author(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture=models.ImageField()
    def __str__(self):
        return self.user.username

class Category(models.Model):
    title=models.CharField(max_length=20)
    def __str__(self):
        return self.title


class Post(models.Model):
    title=models.CharField(max_length=100)
    overview=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    comment=models.IntegerField(default=0)
    views=models.IntegerField(default=0)
    thumbnail=models.ImageField(upload_to='post_thumbs')
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    categories=models.ManyToManyField(Category)
    featured=models.BooleanField(default=False)
    content=RichTextField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', kwargs={'id': self.id})
    
    def get_update_url(self):
        return reverse('post-update',kwargs={"id":self.id})
    
    def get_delete_url(self):
        return reverse('post-delete',kwargs={'id':self.id})
    @property
    def comments(self):
        return self.comment.all().order_by('-timestamp')

class Comment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    timestamp = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.username
