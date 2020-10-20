from django.urls import path
from .forms import UserLoginForm
from .views import SignUpView, UpdatedLoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(),name='signup'),
    path('login/', UpdatedLoginView.as_view(), name='login'),
]