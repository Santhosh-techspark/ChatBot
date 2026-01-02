from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("new-chat/", views.new_chat, name="new_chat"),
    path("chat/<int:conversation_id>/", views.home, name="conversation"),
    path(
    "chat/<int:conversation_id>/delete/",
    views.delete_conversation,
    name="delete_conversation"
),

]
