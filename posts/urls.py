from django.urls import path

from posts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new-post/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.post_like, name='post_like'),
    path('dislike/<int:post_id>/', views.post_dislike, name='post_dislike'),

]
