from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/',views.signup_view, name='signup'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_post, name='create_post'),

    path('my_blogs/', views.my_blogs, name='my_blogs'),
    path('categories/',views.categories,name='categories'),
    path('category/<int:category_id>/', views.category_blogs, name='category_blogs'),

    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),

    path('article/<int:post_id>/', views.article_detail, name='article_detail'),

    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('edit-bio/', views.edit_bio, name='edit_bio'),
]
