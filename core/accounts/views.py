from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True # remeber this warning https://docs.djangoproject.com/en/4.2/topics/auth/default/#django.contrib.auth.views.LoginView.redirect_authenticated_user
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('blog:index')

    def get_success_url(self):
        return reverse_lazy("blog:index")
    

class RegisterPage(FormView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("blog:index")
        return super(RegisterPage, self).get(*args, **kwargs)

def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('custom_auth:dashboard'))