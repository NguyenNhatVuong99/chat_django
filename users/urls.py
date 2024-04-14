from users import views
from django.urls import path

urlpatterns = [
    path('users', views.UserAPIView.as_view()),
    path("users/<slug:id_slug>", views.UserDetailAPIView.as_view()),
    path('auth/register', views.RegisterView.as_view(), name='register'),
    path('auth/login', views.LoginView.as_view(), name='login'),
]
