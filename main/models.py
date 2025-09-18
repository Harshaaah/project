# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.hashers import make_password



# class Client(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to built-in User
#     age = models.IntegerField(null=True, blank=True)
#     interest = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return self.user.username



# class Counsellor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to built-in User
#     age = models.IntegerField(null=True, blank=True)
#     experience = models.IntegerField(null=True, blank=True)

#     def __str__(self):
#         return self.user.username
# class Client(AbstractUser):
#     age = models.IntegerField(null=True, blank=True)
#     interest = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return self.username

# class Counsellor(models.Model):
    
#     username = models.CharField(max_length=15, blank=True)
#     email = models.CharField(max_length=150, blank=True)
#     age = models.IntegerField(null=True, blank=True)
#     experience = models.IntegerField(null=True, blank=True)
#     def __str__(self):
#         return self.username

# class Counsellor(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255, null=True, blank=True)  # will store hashed password
#     age = models.IntegerField(null=True, blank=True)
#     experience = models.IntegerField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         # Hash the password before saving
#         self.password = make_password(self.password)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.username
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_counsellor = models.BooleanField(default=False)

class Client(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    age = models.IntegerField(null=True, blank=True)
    interest = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.user.username
class Counsellor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('stress_management', 'Stress Management'),
        ('career_guidance', 'Career Guidance'),
        ('mental_health', 'Mental Health Support'),
        ('marriage_relationship', 'Marriage and Relationship'),
        ('addiction', 'Addiction Counselling'),
        ('grief_loss', 'Grief and Loss'),
        ('self_esteem', 'Self-Esteem and Personal Growth'),
        ('family_therapy', 'Family Therapy'),
        ('trauma_ptsd', 'Trauma and PTSD'),
        ('eating_disorders', 'Eating Disorders Support'),
        ('child_adolescent', 'Child and Adolescent'),
        ('anger_management', 'Anger Management'),
        ('mindfulness', 'Mindfulness and Meditation'),
        ('financial_stress', 'Financial Stress'),
        ('lgbtq', 'LGBTQ+ Affirmative Therapy'),
    ]
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="counsellor")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    specialization = models.CharField(max_length=255, choices=SPECIALIZATION_CHOICES, blank=True)

    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Counsellor: {self.user.username}"
from .models import Client, Counsellor

class Notification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.client.user.username}: {self.message}"

# class Booking(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Accepted', 'Accepted'),
#         ('Rejected', 'Rejected'),
#     ]

    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

#     def __str__(self):
#         return f"{self.client.username} booked {self.counsellor.username} on {self.date} at {self.time}"
# models.py
# from django.db import models
# from django.conf import settings

class Booking(models.Model):
    # client = models.ForeignKey("Client", on_delete=models.CASCADE)
    # counsellor = models.ForeignKey("Counsellor", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE)
    # request details
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved")],
        default="pending"
    )
    
    # Counsellor fills this after approval
    approved_date = models.DateField(null=True, blank=True)
    approved_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.user.username} -> {self.counsellor.user.username} ({self.status})"

