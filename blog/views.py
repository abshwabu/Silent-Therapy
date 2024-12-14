from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from backend.models import Post, Category, Tag, Comment, Like
from .serializers import PostSerializer, CategorySerializer, TagSerializer, CommentSerializer, LikeSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Optimize query by using select_related and prefetch_related"""
        return Post.objects.all()\
            .select_related('author')\
            .prefetch_related('categories', 'tags') 

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_pk']
        )

class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        # Remove any existing like/dislike by this user on this post
        Like.objects.filter(
            post_id=self.kwargs['post_pk'],
            user=self.request.user
        ).delete()
        
        serializer.save(
            user=self.request.user,
            post_id=self.kwargs['post_pk']
        )