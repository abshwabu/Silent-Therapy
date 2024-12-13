from rest_framework import serializers
from backend.models import Post, Category, Tag

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

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    categories = CategorySerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 
            'categories', 'tags', 'image',
            'created_at', 'updated_at'
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