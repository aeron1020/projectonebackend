from rest_framework import serializers
from .models import Post, Category, Comment, Like, Project, Technology
from users.models import NewUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    liked_by_user = serializers.SerializerMethodField()
    head_image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('category', 'id', 'title', 'slug', 'author', 'excerpt', 'content', 'status', 'published', 'likes_count', 'liked_by_user', 'head_image')

    def get_liked_by_user(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return False
        return obj.user_has_liked(request.user)

 
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author_name', 'content', 'created_at', 'parent')
        extra_kwargs = {
            'replies': {'required': False},
        }

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'session_key', 'created_at')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_title', 'description', 'slug', 'author', 'created_at', 'updated_at', 'tech_stack']

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'logoUrl']