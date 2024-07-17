from django.contrib.auth.views import LoginView, PasswordChangeView

from .forms import CustomAuthenticationForm, CustomPasswordChangeForm

# Create your views here.


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'admin/login.html'


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
