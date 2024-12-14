from rest_framework import serializers
from backend.models import Post, Category, Tag, Comment, Like
from django.conf import settings

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'value']
        read_only_fields = ['id']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = CategorySerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    def to_representation(self, instance):
        """Convert the image URL to a proper format."""
        ret = super().to_representation(instance)
        if ret['image']:
            # Extract just the media path
            image_path = ret['image'].split('/media/')[-1]
            ret['image'] = f'/media/{image_path}'
        return ret

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 
            'categories', 'tags', 'image',
            'created_at', 'updated_at',
            'comments', 'comments_count',
            'likes_count', 'dislikes_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        tags_data = validated_data.pop('tags', [])
        
        post = Post.objects.create(**validated_data)
        
        # Handle categories
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(
                name=category_data['name']
            )
            post.categories.add(category)
        
        # Handle tags
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(
                name=tag_data['name']
            )
            post.tags.add(tag)
        
        return post 