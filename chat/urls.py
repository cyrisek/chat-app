# chat/urls.py
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('chat/<int:id>-<str:name>', views.chat, name="chat"),
    path('api-auth/', include('rest_framework.urls')),
    path('chat_api/', views.ChatList.as_view()),
    path('chat_api/<int:pk>/', views.ChatDetail.as_view()),
]
