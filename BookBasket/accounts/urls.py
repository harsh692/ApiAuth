from django.urls import path, include
from accounts.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,UserPasswordResetView,UserSendPasswordResetEmailView, UserProfileUpdateView, UserProfileUpdateNameView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('updateprofile/', UserProfileUpdateView.as_view(), name='updateprofile'),
    path('updateprofilename/', UserProfileUpdateNameView.as_view(), name='updateprofilename'),
    path('send-reset-password-email/',UserSendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name = 'reset-password'),
]