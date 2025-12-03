from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .forms import LoginForm

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}



# def login_user(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginForm()
#     return render(request, 'users/login.html', {'form': LoginForm()} )

#
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

