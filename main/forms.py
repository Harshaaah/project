from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import Client
from main.models import Counsellor
# Use your custom user model
from django.core.exceptions import ValidationError

INTEREST_CHOICES = [
    ('career', 'Career'),
    ('finance', 'Finance'),
    ('relationship', 'Relationship'),
    ('health', 'Health'),
]
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    age = forms.IntegerField(required=False)
    interest = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Client  # Use custom user model
        fields = ['username', 'email', 'password1', 'password2', 'age', 'interest']

# class CounsellorRegistrationForm(UserCreationForm):
#     email = forms.EmailField()
#     age = forms.IntegerField(required=False)
#     experience = forms.CharField(max_length=100, required=False)

#     class Meta:
#         model = Client
#         fields = ['username', 'email', 'password1', 'password2', 'age', 'experience']



class CounsellorRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Counsellor
        fields = ['username', 'email', 'password1', 'password2', 'age', 'experience']

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")
        if pw1 != pw2:
            raise ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = self.cleaned_data["password1"]  # For now store as plain (not secure)
        if commit:
            user.save()
        return user
    
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['counsellor', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
