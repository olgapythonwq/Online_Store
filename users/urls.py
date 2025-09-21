from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import CustomLoginView, RegisterView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
