from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class login_tbl(AbstractUser):
    usertype = models.CharField(max_length=100)
    def __str__(self):
        return self.username
    
class Users(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    user=models.ForeignKey(login_tbl,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    
class Clubs(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    image=models.ImageField(upload_to='club_images/')
    description=models.CharField(max_length=100)
    user=models.ForeignKey(login_tbl,on_delete=models.CASCADE,null=True)   

    def __str__(self):
        return self.name
    
class Club_Highlights(models.Model):
    club=models.ForeignKey(Clubs,on_delete=models.CASCADE)
    image=models.ImageField()
    def __str__(self):
        return self.club.name
    

class Events(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('comedy', 'Comedy'),
        ('dance', 'Dance'),
        ('theatre', 'Theatre'),
        ('sports', 'Sports'),
        ('conference', 'Conference'),
        ('exhibition', 'Exhibition'),
        ('festival', 'Festival'),
        ('party', 'Party'),
        ('other', 'Other'),
    ]

    club = models.ForeignKey('Clubs', on_delete=models.CASCADE)
    main_image = models.ImageField(null=True, blank=True, upload_to='event_images/')
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)  # Automatically set on creation
    event_at = models.DateTimeField()
    description = models.TextField()  # Use TextField for long descriptions
    address = models.CharField(max_length=200)  # Increased max length for flexibility
    capacity = models.IntegerField()  # Ensure non-negative values
    price = models.PositiveIntegerField()  # Normal ticket price
    vip_price = models.PositiveIntegerField(null=True, blank=True)  # Optional VIP ticket price
    vip_capacity = models.PositiveIntegerField(null=True, blank=True)  # Optional VIP ticket capacity
    vip_description = models.TextField(null=True, blank=True)  # Optional VIP description
    event_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True)
    artist = models.CharField(max_length=100, null=True, blank=True)
    lattitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)

    def __str__(self):
        return f"{self.name} ({self.event_at.strftime('%Y-%m-%d')})"


    
class Booking(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    event=models.ForeignKey(Events,on_delete=models.CASCADE)
    nquantity=models.IntegerField(null=True,blank=True)
    vquantity=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.user.name 

