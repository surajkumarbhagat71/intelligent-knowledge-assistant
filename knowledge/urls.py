from django.urls import path

from .views import *


urlpatterns = [
    path("chat/", chat, name="knowledge-chat"),
    path("ai-agent/", agent_chat, name="agent_chat"),
    
]






