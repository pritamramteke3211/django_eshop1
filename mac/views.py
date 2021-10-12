from django.shortcuts import render,redirect
from django.views import View
from shop.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import  *
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from shop.forms import SignupForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import *



class HomePage(View):
    template_name = 'mhome.html'
    def get(self, request):
        return render(request,self.template_name)
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User Create Successfully')
            return redirect('login')
    else:
        form = SignupForm()
    context = {'form':form}
    return render(request,'signup.html',context)

def prac(request):
    return render(request,'prac.html')

def jsondata(request):
    data = list(Cart.objects.filter(user=request.user).values())
    return JsonResponse(data,safe = False)

class MyLoginView(LoginView):
    template_name='login.html'
    # authentication_form=LoginForm
    
class MyLogoutView(LogoutView):
    template_name='logout.html'
    
class MyPasswordChangeView(PasswordChangeView):
    template_name='changepass.html'
    # success_url='/password_change_done/'
    
class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name='password_change_done.html'


class MyPasswordResetView(PasswordResetView):
    template_name='password_reset.html'

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name='password_reset_done.html'

class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='password_reset_confirm.html'

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name='password_reset_complete.html'