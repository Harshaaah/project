from django.db import models
from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    interest = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username

class Counsellor(models.Model):
    username = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=150, blank=True)
    age = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.username



from .models import Client, Counsellor

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.client.username} booked {self.counsellor.username} on {self.date} at {self.time}"


# models.py
# from django.db import models
# from django.contrib.auth.models import User
# from .models import Counsellor  # Assuming you already have a Counsellor model

# class Booking(models.Model):
#     client = models.ForeignKey(User, on_delete=models.CASCADE)  # Logged-in user
#     counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
    
#     STATUS_CHOICES = (
#         ('Pending', 'Pending'),
#         ('Confirmed', 'Confirmed'),
#         ('Cancelled', 'Cancelled'),
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

#     def __str__(self):
#         return f"{self.client.username} booked {self.counsellor} on {self.date} at {self.time}"
