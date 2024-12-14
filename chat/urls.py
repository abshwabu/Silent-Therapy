from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'private', views.PrivateChatViewSet, basename='private-chat')
router.register(r'group', views.GroupChatViewSet, basename='group-chat')

app_name = 'chat'

urlpatterns = [
    path('', include(router.urls)),
]
