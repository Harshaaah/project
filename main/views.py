from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import UserRegistrationForm
from .forms import CounsellorRegistrationForm

def home(request):
    return render(request, 'home.html')

# def login_view(request):
#     user=None
#     error_message=None
#     if request.POST:
#         username=request.POST['username']
#         password=request.POST['password']
#         try:
#             user=User.objects.create_user(username=username, password=password)
#         except Exception as e:
#             error_message = str(e)
#     return render(request, 'login.html',{user:user,'error_message':error_message})

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('book_counsellor')  # ✅ Change to the actual name of your booking URL
        else:
            error_message = "Invalid username or password."

    return render(request, 'login.html', {'error_message': error_message})


def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            return redirect('login')  # Replace with your desired redirect
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': user_form})


def register_counselor(request):
    if request.method == 'POST':
        counselor_form = CounsellorRegistrationForm(request.POST)
        if counselor_form.is_valid():
            counselor_form.save()
            # user.set_password(counselor_form.cleaned_data['password1'])
            # user.save()
            return redirect('login')  # Redirect to login or dashboard
        else:
            print("Form errors:", counselor_form.errors)
    else:
      
        counselor_form = CounsellorRegistrationForm()
    return render(request, 'accounts/registercounsellor.html', {
        'counselor_form': counselor_form
    })


from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def book_counsellor(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user  # assuming logged in user is Client
            booking.status = 'Pending'
            booking.save()
            return redirect('client_dashboard')  # or any success page
    else:
        form = BookingForm()
    return render(request, 'book_counsellor.html', {'form': form})

def client_dashboard(request):
    return render(request, 'client_dashboard.html')

def counsellor_dashbord(request):
    return render(request, 'counsellor_dashboard.html')