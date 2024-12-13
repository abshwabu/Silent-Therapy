from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RoomViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')

# Add custom actions to the router
room_message_list = RoomViewSet.as_view({
    'get': 'list_messages',
    'post': 'create_message'
})

urlpatterns = [
    path('', include(router.urls)),
    # Add message endpoints
    path('rooms/<int:pk>/messages/', room_message_list, name='room-messages'),
]
