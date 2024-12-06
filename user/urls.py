from django.urls import path
from .views import login_user, user_registration, logout_user


urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', user_registration, name='register'),
    path('logout/', logout_user, name='logout'),
]