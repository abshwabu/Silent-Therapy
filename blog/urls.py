from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'tags', views.TagViewSet, basename='tag')

# Create nested routers for comments and likes
posts_router = routers.NestedDefaultRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', views.CommentViewSet, basename='post-comments')
posts_router.register(r'likes', views.LikeViewSet, basename='post-likes')

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
] 