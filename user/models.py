from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    LIVE = 0
    DELETE = 0
    DELETE_CHOICES = ((LIVE,'Live'),(DELETE,'Delete'))

    name = models.CharField(max_length=200)
    #profle creation
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='customer_profile')

    #extra
    image = models.ImageField(upload_to='images/user_image/',null=True) 
    # phone = models.CharField(max_length=20)
    address = models.TextField()
    place = models.CharField(max_length=30)
    pin = models.CharField(max_length=10)
    dob = models.DateField(null=True)

   
    
    

    deleted_status = models.IntegerField(choices=DELETE_CHOICES ,default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self)->str:
        return self.name
    




class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserSkill(models.Model):
    LIVE = 0
    DELETE = 1
    STATUS_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)
    proficiency_level = models.IntegerField(default=0)  # Example additional field

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.get_status_display()})"
    





class Destination(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserDestination(models.Model):
    LIVE = 0
    DELETE = 1
    STATUS_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)
    

    class Meta:
        unique_together = ('user', 'destination')

    def __str__(self):
        return f"{self.user.username} - {self.destination.name} ({self.get_status_display()})"