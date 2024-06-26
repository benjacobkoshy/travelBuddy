from django.db import models
from user.models import Customer

class Advertisement(models.Model):
    LIVE = 0
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    name = models.CharField(max_length=200,null=False)
    description = models.TextField(null=False)
    terms_condition = models.TextField(null=False)
    location = models.CharField(max_length=100,null=False)

    mobile_number = models.CharField(max_length=15, null=False, blank=True)
    email = models.EmailField(null=False, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)

    deleted_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional fields for images and videos
    images = models.ImageField(upload_to='images/advertisement/', null=True,blank=True)
    video = models.FileField(upload_to='video/advertisement/', null=True,blank=True)


    owner = models.ForeignKey(Customer,on_delete=models.SET_NULL,related_name='advertisement_owner',null=True)


    def __str__(self):
        return self.name
