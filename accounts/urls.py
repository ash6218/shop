from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('update_profile/', views.UserUpdateProfileView.as_view(), name='update_profile'),
    path('change_password/', views.UserChangePasswordView.as_view(), name='change_password'),
    path('reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('otplogin/', views.UserOtpLoginView.as_view(), name='user_otplogin'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('loginverify/', views.UserLoginVerifyCodeView.as_view(), name='login_verify_code'),
    path('upload_profile/', views.UploadProfileImageView.as_view(), name='upload_profile'),
    path('change_sms_form/', views.ChangeSmsFormView.as_view(), name='change_sms_form'),
    path('api_register/', views.ApiRegisterView.as_view(), name='api_register'),
]