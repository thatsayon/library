from django.urls import path 
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserAccountUpdateView, returnbook

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='Register'),
    path('login/', UserLoginView.as_view(), name='Login'),
    path('logout/', UserLogoutView.as_view(), name='Logout'),
    path('profile/', UserAccountUpdateView.as_view(), name='Profile'),
    path('return/<int:id>/', returnbook, name='Return'),
]
