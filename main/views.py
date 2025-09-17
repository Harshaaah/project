from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import ClientRegisterForm
from .forms import CounsellorRegisterForm
from .models import Client, Counsellor,Booking
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
from django.contrib import messages
def login_view(request):
    

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Redirect based on profile type
            if user.is_client and hasattr(user, 'client'):
            # if user.is_client:
                return redirect("client_dashboard")
            elif user.is_counsellor and hasattr(user, 'counsellor'):
            # elif user.is_counsellor:
                return redirect("counsellor_dashboard")
            else:
                messages.error(request, "Profile not set up. Contact admin.")
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            
            return redirect("login")
    return render(request, 'login.html')

    #     if user is not None:
    #         login(request, user)
    #         if Client.objects.filter(username=user).exists():
    #             messages.success(request, f"Welcome back, {user.username}!")
    #             return redirect('client_dashboard')  # your URL name

    #         # 🔍 Check if the logged in user is a Counsellor
    #         elif Counsellor.objects.filter(username=user).exists():
    #             messages.success(request, f"Welcome back, {user.username}!")
    #             return redirect('counsellor_dashboard')  # your URL name

    #         # Optional: if neither, show error
    #         else:
    #             error_message = "User type not recognized."
          
    #     else:
    #         error_message = "Invalid username or password."

    # return render(request, 'login.html', {'error_message': error_message})


    #     if user is not None:
    #         login(request, user)
    #         if Client.objects.filter(username=user.username).exists():
    #             messages.success(request, f"Welcome back, {user.username}!")
    #             return redirect('client_dashboard')
    #         else:
    #             messages.error(request, "User type not recognized.")
    #             return redirect('login')

    #     # 2️⃣ Try Counsellor authentication via custom backend
    #     counsellor = authenticate(
    #         request,
    #         username=username,
    #         password=password,
    #         backend='myapp.backends.CounsellorBackend'
    #     )
    #     if counsellor:
    #         request.session['counsellor_id'] = counsellor.id
    #         messages.success(request, f"Welcome back, {counsellor.username}!")
    #         return redirect('counsellor_dashboard')

    #     # 3️⃣ If both fail
    #     messages.error(request, "Invalid username or password.")

    # return render(request, 'login.html')
from .models import User, Client, Counsellor

def register_user(request):
    if request.method == 'POST':
        user_form = ClientRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_client = True   # Mark as client
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            # Create Client profile
            Client.objects.create(
                user=user,
                age=user_form.cleaned_data.get('age'),
                interest=user_form.cleaned_data.get('interest')
            )

            messages.success(request, 'Registration successful! Welcome, client!')
            return redirect('login')
    else:
        user_form = ClientRegisterForm()
    return render(request, 'accounts/register.html', {'form': user_form})


def register_counselor(request):
    if request.method == 'POST':
        counselor_form = CounsellorRegisterForm(request.POST)
        if counselor_form.is_valid():
            user = counselor_form.save(commit=False)
            user.is_counsellor = True   # Mark as counsellor
            user.set_password(counselor_form.cleaned_data['password1'])
            user.save()

            # Create Counsellor profile
            Counsellor.objects.create(
                user=user,
                age=counselor_form.cleaned_data.get('age'),
                experience=counselor_form.cleaned_data.get('experience'),
                specialization =counselor_form.cleaned_data.get('specialization'),
                description =counselor_form.cleaned_data.get('description', '').strip()
            )

            messages.success(request, 'Registration successful! Welcome, counsellor!')
            return redirect('login')
        else:
            print("Form errors:", counselor_form.errors)
    else:
        counselor_form = CounsellorRegisterForm()
    return render(request, 'accounts/registercounsellor.html', {
        'counselor_form': counselor_form
    })


# def register_user(request):
#     if request.method == 'POST':
#         user_form = ClientRegisterForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password1'])
#             user.save()
#             messages.success(request, 'Registration successful! Welcome, client!')
#             return redirect('login')  # Replace with your desired redirect
#     else:
#         user_form = ClientRegisterForm()
#     return render(request, 'accounts/register.html', {'form': user_form})


# def register_counselor(request):
#     if request.method == 'POST':
#         counselor_form = CounsellorRegisterForm(request.POST)
#         if counselor_form.is_valid():
#             counselor_form.save()
#             messages.success(request, 'Registration successful! Welcome, counsellor!')
#             # user.set_password(counselor_form.cleaned_data['password1'])
#             # user.save()
#             return redirect('login')  # Redirect to login or dashboard
#         else:
#             print("Form errors:", counselor_form.errors)
#     else:
      
#         counselor_form = CounsellorRegisterForm()
#     return render(request, 'accounts/registercounsellor.html', {
#         'counselor_form': counselor_form
#     })


from django.shortcuts import render, redirect
from .forms import BookingForm

from django.contrib.auth.decorators import login_required

# @login_required
# def book_counsellor(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.client = request.user.client  # assuming logged in user is Client
#             booking.status = 'Pending'
#             booking.save()
#             return redirect('client_dashboard')  # or any success page
#     else:
#         form = BookingForm()
#     return render(request, 'book_counsellor.html', {'form': form})

# views.py
from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking

def book_counsellor(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user.client   # set client
            booking.counsellor = form.cleaned_data['counsellor']  # set counsellor
            booking.status = "pending"  # set default status
            booking.save()
            return redirect('client_dashboard')
    else:
        form = BookingForm()
    return render(request, 'book_counsellor.html', {'form': form})


# def recommend_articles(interest):
#     # You can replace this with your actual AI logic later
#     if 'stress' in interest.lower():
#         return ["5 Ways to Manage Stress", "Meditation Techniques for Relaxation"]
#     elif 'career' in interest.lower():
#         return ["Top Career Planning Tips", "How to Set Career Goals"]
#     else:
#         return ["How to Stay Positive Daily", "Benefits of Talking to a Therapist"]

@login_required
def client_dashboard(request):    
    client = request.user.client  # get the logged-in client user
    message = None

    # When form is submitted
    if request.method == 'POST':
        new_interest = request.POST.get('new_interest')  # get new interest
        if new_interest:
            # If client has existing interests
            if client.interest:
                # Add new interest to existing list
                client.interest += f", {new_interest}"
            else:
                client.interest = new_interest  # First interest
            client.save()  # Save updated client
            message = "Interest added successfully!"

    # Split interests into a list
    if client.interest:
        interests = client.interest.split(",")
    else:
        interests = []

    # Generate article titles from interests
    articles = []
    for interest in interests:
        interest = interest.strip()
        if interest:
            articles.append(f"AI article about {interest}")

    # Get all bookings for this client
    bookings = Booking.objects.filter(client=client)

    # Get all counsellors
    counsellors = Counsellor.objects.all()

    return render(request, 'dashboards/client_dashboard.html', {
        'client': client,
        'interests': interests,
        'articles': articles,
        'bookings': bookings,
        'counsellors': counsellors,
        'message': message,
        
    })

# views.py
# from django import forms

# class BookingApprovalForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['approved_date', 'approved_time', 'status']

# @login_required
# def counsellor_dashboard(request):
#     if request.user.is_counsellor:
#         bookings = Booking.objects.filter(counsellor=request.user)
#     else:
#         bookings = [] 
#     # bookings = Booking.objects.all()
#     return render(request, 'dashboards/counsellor_dashboard.html', {'bookings': bookings})

from .models import Booking, Counsellor

def counsellor_dashboard(request):
    if request.user.is_counsellor:
        counsellor_profile = Counsellor.objects.get(user=request.user)
        bookings = Booking.objects.filter(counsellor=counsellor_profile)
    else:
        bookings = []

    return render(request, 'dashboards/counsellor_dashboard.html', {'bookings': bookings})


# @login_required
# def approve_booking(request, booking_id):
#     booking = Booking.objects.get(id=booking_id, counsellor=request.user.counsellor)
#     # booking = get_object_or_404(Booking, id=booking_id, counsellor=request.user.counsellor)
#     if request.method == "POST":
#         form = BookingApprovalForm(request.POST, instance=booking)
#         if form.is_valid():
#             form.instance.status = "Approved"
#             form.save()
#             return redirect('counsellor_dashboard')
#     else:
#         form = BookingApprovalForm(instance=booking)
#     return render(request, 'approve_booking.html', {'form': form})
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, counsellor=request.user.counsellor)

    if request.method == "POST":
        # get date & time from form
        approved_date = request.POST.get('date')
        approved_time = request.POST.get('time')

        # update booking
        booking.approved_date = approved_date
        booking.approved_time = approved_time
        booking.status = "Approved"
        booking.save()

        # redirect to dashboard
        return redirect('counsellor_dashboard')

    # if GET → just show the form
    return render(request, 'approve_booking.html', {"booking": booking})


# @login_required
# def counsellor_dashbord(request):
#     return render(request, 'dashboards/counsellor_dashboard.html')
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')  # Redirect to a logout confirmation page or home page

# 
# import os
# import pandas as pd
# from django.conf import settings
# from django.shortcuts import render
# from .models import Client

# def recommend_articles(request):
#     # Build full path for dataset
#     file_path = os.path.join(settings.BASE_DIR, "articles.csv")

#     # Load dataset
#     df = pd.read_csv(file_path)

#     # Get client interests
#     client = Client.objects.get(user=request.user)
#     interests = client.interest.split(",") if client.interest else []

#     # Filter dataset: keep only articles matching interests
#     recommended = df[df['category'].isin([i.strip() for i in interests])]

#     # Convert filtered articles to dictionary for template
#     articles = recommended.to_dict(orient="records")

#     # Render the template with the articles data
#     return render(request, "recommend_articles.html", {"articles": articles})


# import os
# import pandas as pd
# from django.conf import settings
# from django.shortcuts import render
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from .models import Client

# def recommend_articles(request):
#     # Step 1: Get the client's interests
#     client = Client.objects.get(user=request.user)
#     interests = client.interest.split(",") if client.interest else []
    
#     # Step 2: Load the dataset
#     file_path = os.path.join(settings.BASE_DIR, "articles.csv")
#     df = pd.read_csv(file_path)

#     # Step 3: Combine title and description for better analysis
#     df['content'] = df['title'] + " " + df['description']

#     # Step 4: Use TF-IDF to vectorize the content
#     vectorizer = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = vectorizer.fit_transform(df['content'])

#     # Step 5: Convert interests into one string
#     interest_text = " ".join(interests)

#     # Step 6: Vectorize the interest
#     interest_vec = vectorizer.transform([interest_text])

#     # Step 7: Compute similarity scores
#     similarities = cosine_similarity(interest_vec, tfidf_matrix).flatten()

#     # Step 8: Add the similarity score to the dataframe
#     df['score'] = similarities

#     # Step 9: Sort articles by similarity score
#     recommended = df.sort_values(by='score', ascending=False)

#     # Step 10: Convert to list of dicts for template
#     articles = recommended.to_dict(orient='records')

#     return render(request, "recommend_articles.html", {"articles": articles, "interests": interests})

# import os
# import pandas as pd
# from django.conf import settings
# from django.shortcuts import render
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from .models import Client

# def recommend_articles(request):
#     # Step 1: Get the client's interests
#     client = Client.objects.get(user=request.user)
#     interests = client.interest.split(",") if client.interest else []
    
#     # Step 2: Load the dataset
#     file_path = os.path.join(settings.BASE_DIR, "articles.csv")
#     df = pd.read_csv(file_path)

    

#     if not interests or df.empty:
#         articles = []
#     else:
#         # Step 3: Combine title and description for better context
#         df['content'] = df['title'] + " " + df['description']

#         # Step 4: Vectorize the article contents using TF-IDF
#         vectorizer = TfidfVectorizer(stop_words='english')
#         tfidf_matrix = vectorizer.fit_transform(df['content'])

#         # Step 5: Convert interests into one string and vectorize it
#         interest_text = " ".join(interests)
#         interest_vec = vectorizer.transform([interest_text])

#         # Step 6: Compute cosine similarity between interests and articles
#         similarities = cosine_similarity(interest_vec, tfidf_matrix).flatten()

#         # Step 7: Add similarity score to the DataFrame
#         df['score'] = similarities

#         # Step 8: Sort articles by similarity score in descending order
#         recommended = df.sort_values(by='score', ascending=False)

#         # Optional: Show only top 5 or relevant articles with a minimum threshold
#         recommended = recommended[recommended['score'] > 0].head(5)

#         # Step 9: Convert to dictionary format for the template
#         articles = recommended.to_dict(orient='records')

#     return render(request, "recommend_articles.html", {"articles": articles, "interests": interests})


# import os
# import pandas as pd
# from django.shortcuts import render
# from django.conf import settings
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from .models import Client

# def recommend_articles(request):
#     # Get user interests
#     client = Client.objects.get(user=request.user)
#     interests = client.interest.split(",") if client.interest else []
#     interests = [i.strip() for i in interests]

#     # Load dataset
#     file_path = os.path.join(settings.BASE_DIR, "articles.csv")
#     df = pd.read_csv(file_path)

#     # Combine title and description
#     df['content'] = df['title'] + " " + df['description']
#     documents = df['content'].tolist()
#     user_input = " ".join(interests)
#     documents.append(user_input)

#     # Vectorize
#     vectorizer = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = vectorizer.fit_transform(documents)

#     # Compute similarity
#     cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
#     df['similarity'] = cosine_sim

#     # Get top 5 recommendations
#     recommended = df.sort_values(by='similarity', ascending=False).head(5)
#     articles = recommended.to_dict(orient='records')

#     context = {
#         'articles': articles,
#         'interests': ", ".join(interests)
#     }

#     return render(request, 'recommend_articles.html', context)

# views.py
import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from .models import Client

def recommend_articles(request):
    # Step 1: Get the logged-in client's interests
    client = Client.objects.get(user=request.user)
    interests = client.interest.split(",") if client.interest else []
    interests = [i.strip().lower() for i in interests]  # Clean up spaces and case

    # Step 2: Load the dataset from CSV
    file_path = os.path.join(settings.BASE_DIR, 'articles.csv')
    df = pd.read_csv(file_path)

    # Step 3: Filter articles by matching categories with interests
    df['category'] = df['category'].str.lower()  # Convert categories to lowercase
    recommended = df[df['category'].isin(interests)]

    # Step 4: Pass the recommended articles to the template
    articles = recommended.to_dict('records')  # Convert to list of dictionaries
    return render(request, 'recommend_articles.html', {'articles': articles})


from .forms import ClientProfileForm, CounsellorProfileForm
@login_required
def client_profile(request):
    # make sure only clients can access
    if not hasattr(request.user, 'client'):
        return redirect('login')

    client = request.user.client  # get client profile

    if request.method == "POST":
        # take form data from POST request
        form = ClientProfileForm(request.POST)
        if form.is_valid():
            # update User table
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # update Client table
            client.age = form.cleaned_data['age']
            client.interest = form.cleaned_data['interest']
            client.save()

            return redirect('client_profile')  # refresh page after save
    else:
        # show existing values in the form
        form = ClientProfileForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'age': client.age,
            'interest': client.interest
        })

    return render(request, 'profiles/client_profile.html', {'form': form})

@login_required
def counsellor_profile(request):
    # make sure only counsellors can access
    if not hasattr(request.user, 'counsellor'):
        return redirect('login')

    counsellor = request.user.counsellor  # get counsellor profile

    if request.method == "POST":
        form = CounsellorProfileForm(request.POST)
        if form.is_valid():
            # update User table
            request.user.username = form.cleaned_data['username']
            request.user.email = form.cleaned_data['email']
            request.user.save()

            # update Counsellor table
            counsellor.age = form.cleaned_data['age']
            counsellor.experience = form.cleaned_data['experience']
            counsellor.save()

            return redirect('counsellor_profile')
    else:
        form = CounsellorProfileForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'age': counsellor.age,
            'experience': counsellor.experience
        })

    return render(request, 'profiles/counsellor_profile.html', {'form': form})

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking canceled successfully!")
    return redirect('client_dashboard')  # replace with your dashboard url name