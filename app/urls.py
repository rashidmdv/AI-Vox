"""
URL configuration for voice_chatgpt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import  views
from .views import send_complaint_post

urlpatterns = [
    path('', views.login),
    path('login_submit', views.login_submit),
    path('forget_password',views.forget_password),
    path('forget_password_post',views.forget_password_post),
    # path('new_password/<username>',views.new_password),

    path('logout',views.logout),


#ADMIN

    path('admin-dashboard', views.home),
    path('view_user', views.view_user),
    path('accept_user/<id>', views.accept_user),
    path('reject_user/<id>', views.reject_user),
    path('edit_user_action/<id>', views.edit_user_action),
    path('view_complaint', views.view_complaint),
    path('send_reply/<id>',views.send_reply),
    path('view_review', views.view_review),

# USER
    path('user_home',views.user_home),
    path('register',views.register),
    path('register_post', views.register_post),
    path('chat',views.chatbot),
    path('mychatbot',views.my_chatbot),
    path('image_generation',views.image_generation),
    path('image_generation_post',views.image_generation_post),
    path('all_complaints',views.all_complaints),
    path('send_complaint',views.send_complaint),
    path('send_review',views.send_review),
    path('view_cmp_reply',views.view_cmp_reply),
    path('send_complaint_post',views.send_complaint_post),
    path('send_review_post',views.send_review_post),
    path('profile/', views.profile),
    path('update_profile', views.update_profile),
    path('user_pay_proceed',views.user_pay_proceed),
    path('on_payment_success',views.on_payment_success),



    path('chatbot-response/', views.chatbot_response, name="chatbot_response"),


]

