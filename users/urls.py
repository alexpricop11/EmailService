from django.urls import path
from users.views import UserRegisterView, UserLoginView

urlpatterns = [
    path("signup", UserRegisterView.as_view()),
    path("signin", UserLoginView.as_view()),
]
