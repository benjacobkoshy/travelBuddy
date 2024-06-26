from django.db import models
from user.models import Customer
# Create your models here.

class CreateVideo(models.Model):

    LIVE = 0
    DELETE = 0
    DELETE_CHOICES = ((LIVE,'Live'),(DELETE,'Delete'))

    video  = models.FileField(upload_to='video/short-video/',null=True)
    owner = models.ForeignKey(Customer,on_delete=models.SET_NULL,related_name='video_owner',null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)

    deleted_status = models.IntegerField(choices=DELETE_CHOICES ,default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)