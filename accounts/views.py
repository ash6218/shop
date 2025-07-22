from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserCreationForm, VerifyCodeForm, UserLoginForm, UserOtpLoginForm
import random, pytz
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import send_otp_code_task
from shop import settings

class UserRegisterView(View):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    def get(self, request):
        form = self.form_class # no prantesis is needed
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(10000, 99999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number' : form.cleaned_data['phone_number'],
                'email' : form.cleaned_data['email'],
                'full_name' : form.cleaned_data['full_name'],
                'password' : form.cleaned_data['password1'], # might have error here!!!
            }
            messages.success(request, 'we sent you a code.', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form':form})
    

class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form':form})


    def post(self, request):
        expiration_seconds = 120
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number = user_session['phone_number'])
        form = self.form_class(request.POST)
        expire_check = datetime.now(pytz.timezone('UTC')) - code_instance.created
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code and expire_check < timedelta(seconds=expiration_seconds) :
                User.objects.create_user(user_session['phone_number'], 
                                         user_session['email'], 
                                         user_session['full_name'], 
                                         user_session['password'])
                code_instance.delete()
                messages.success(request, 'you registered successfully', 'success')
            elif cd['code'] == code_instance.code and expire_check > timedelta(seconds=expiration_seconds) :
                messages.error(request, 'this code is expired, please try again.', 'danger')
                code_instance.delete()
                return redirect('accounts:verify_code')
            else:
                messages.error(request, 'this code is wrong.', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,f'welcome {user.email}. you logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'Username or Password is not correct!', 'warning')
        return render(request, self.template_name, {'form':form})
    

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request): 
        logout(request)
        messages.success(request, 'you logged out successfully','success')
        return redirect('home:home')
    
class UserOtpLoginView(View):
    form_class = UserOtpLoginForm
    template_name = 'accounts/otplogin.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            random_code = random.randint(1000, 9999)
            if settings.CELERY_IS_ACTIVE:
                send_otp_code_task.delay(form.cleaned_data['phone_number'], random_code)
            else:
                send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_otplogin_info'] = {'phone_number' : form.cleaned_data['phone_number']}
            messages.success(request, 'we sent you a code.', 'success')
            return redirect('accounts:login_verify_code')
        return render(request, self.template_name, {'form':form})


class UserLoginVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/otplogin.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        expiration_seconds = 120
        form = self.form_class(request.POST)
        user_session = request.session['user_otplogin_info']
        if form.is_valid():
            phone = user_session['phone_number']
            code_instance = OtpCode.objects.get(phone_number = phone)
            expire_check = datetime.now(pytz.timezone('UTC')) - code_instance.created
            user = User.objects.filter(phone_number=phone).first() # this is important to get None instead of DoesNotExsitsError, also no leakage!
            if user is not None and code_instance.code == form.cleaned_data['code'] and expire_check < timedelta(seconds=expiration_seconds):
                login(request,user)
                code_instance.delete()
                messages.success(request,f'welcome {user.email}. you logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            elif user is not None and expire_check > timedelta(seconds=expiration_seconds) :
                messages.error(request, 'this code is expired, please try again.', 'danger')
                code_instance.delete()
                return redirect('accounts:user_otplogin')
            messages.error(request, 'Username or OTP-Code is not correct!', 'warning')
            return redirect('accounts:login_verify_code')
        return render(request, self.template_name, {'form':form})
