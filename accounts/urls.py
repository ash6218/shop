from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('otplogin/', views.UserOtpLoginView.as_view(), name='user_otplogin'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('loginverify/', views.UserLoginVerifyCodeView.as_view(), name='login_verify_code'),
    
]