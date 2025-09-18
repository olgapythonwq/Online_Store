from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomUserCreationForm, UserProfileForm
from django.core.mail import send_mail  # стандартный метод Django, чтобы отправлять сообщения
from django.contrib.auth import login
from .forms import EmailAuthenticationForm
from .models import CustomUser


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        user = form.save()  # получаем пользователя
        login(self.request, user)  # Пользователь автоматически авторизуется после регистрации
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Welcome to our Online Store'
        message = 'Thank you for your registration in our Online Store!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email,]
        send_mail(subject, message, from_email, recipient_list)


class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'users/login.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self):
        return self.request.user
