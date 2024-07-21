# backend/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import ChatBotViewSet

router = DefaultRouter()
router.register(r'chats', ChatBotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('chats/ask_question/', ChatBotViewSet.as_view({'post': 'ask_question'}), name='ask-question'),
]
