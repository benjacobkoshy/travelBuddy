from django.db import models
from user.models import Customer
from django.contrib.auth.models import User
from datetime import datetime



class Message(models.Model):
 

    # LIVE = 0
    # DELETE = 0
    # DELETE_CHOICES = ((LIVE,'Live'),(DELETE,'Delete'))

    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    # deleted_status = models.IntegerField(choices=DELETE_CHOICES ,default=LIVE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"From {self.sender.name} to {self.receiver.name} - {self.timestamp}"
