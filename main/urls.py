from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/client', views.register_user, name='register'),
    path('registercounsellor/', views.register_counselor, name='registercounsellor'),
    path('book_counsellor/', views.book_counsellor, name='book_counsellor'),
    path('client_dashboard/',views.client_dashboard, name='client_dashboard'),
    path('counsellor_dashboard/',views.counsellor_dashboard, name='counsellor_dashboard'),
    path('approve_booking/<int:booking_id>/',views.approve_booking, name='approve_booking'),
    path('logout/',views.logout_view, name='logout'),
    path('articles/',views.recommend_articles, name='recommend_articles'),
    path("client/profile/", views.client_profile, name="client_profile"),
    path("counsellor/profile/", views.counsellor_profile, name="counsellor_profile"),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

]


