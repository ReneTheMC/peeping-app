from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from accounts import views

urlpatterns = [
    path('edit/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('<str:username>/', views.profile, name='profile'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),

]