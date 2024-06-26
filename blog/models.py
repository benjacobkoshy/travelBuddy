from django.db import models
from user.models import Customer
# from . models import Blog
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    LIVE = 0
    DELETE = 0
    DELETE_CHOICES = ((LIVE,'Live'),(DELETE,'Delete'))
    header = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/upload_image/',null=True)
    # video = models.FileField(upload_to='video/',null=True)

    owner = models.ForeignKey(Customer,on_delete=models.SET_NULL,related_name='owner',null=True)

    author = models.CharField(max_length=100)
    yourself = models.TextField()

    likes = models.ManyToManyField(Customer,related_name='blog_post')

    deleted_status = models.IntegerField(choices=DELETE_CHOICES ,default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def total_likes(self):
        return self.likes.count()

    def __str__(self)->str:
        return self.title
    
#comment section
class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comment" ,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="comment_owner" ,on_delete=models.CASCADE)
    text = models.TextField() 
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.blog.title,self.user)
