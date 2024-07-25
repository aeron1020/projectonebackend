from rest_framework import generics
from .serializers import PostSerializer, UserSerializer, CommentSerializer, ProjectSerializer, CategorySerializer, TechnologySerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import filters
from rest_framework import permissions
from django.db.models import Q
from .models import Post, Comment, Like, Project, Category, Technology
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import NewUser
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordChangeSerializer


class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return True
        
        return obj.author == request.user
    
class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update user instance.
    """
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
   
    def get_object(self):
        print(self.request.user)
        # Return the user associated with the current request
        return self.request.user

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class PostList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer
    # queryset = Post.objects.all()

    # def get_queryset(self):
    #     return Post.objects.filter(Q(deleted=False) & Q(status='published'))
    def get_queryset(self):
        queryset = Post.objects.filter(deleted=False, status='published')
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset


class PostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer
    lookup_field = 'slug'  # Set the lookup field to 'slug'
    
    def get_queryset(self):
        # slug = self.request.query_params.get('slug', None)
        
        slug = self.kwargs.get('slug', None)

        user = self.request.user

        print(user)

        return Post.objects.filter(slug=slug, deleted=False, status='published')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

       
class PostListDetailFilter(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']

class UserPostsList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter posts by the author's ID
        return Post.objects.filter(author=self.request.user, deleted=False, status='published')


class CreatePost(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser) 

    def perform_create(self, serializer):
        category_id = self.request.data.get('category')
        category = get_object_or_404(Category, pk=category_id)
        # Set the author of the post to the current user
        # serializer.save(author=self.request.user)
        serializer.save(author=self.request.user, category=category)
        
class AdminPostDetails(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class EditPost(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, PostUserWritePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, PostUserWritePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_destroy(self, instance):
        # Override the perform_destroy method to add additional logic
        # For example, you can add a flag to mark the post as deleted instead of actually deleting it from the database
        instance.deleted = True
        instance.save()


class PostCommentsList(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Get the post ID from the URL parameters
        post_id = self.kwargs.get('pk')
        # Filter comments by the post's ID
        queryset = Comment.objects.filter(post_id=post_id)
        return queryset
    

class CreateComment(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, PostUserWritePermission]


from django.utils.crypto import get_random_string

class CreateCommentForGuest(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    # Override perform_create to handle unauthenticated user case
    def perform_create(self, serializer):
        # Get the session key
        session_key = self.request.session.session_key
        
        # If session key exists, use its first 4 characters as the guest name
        if session_key:
            guest_name = session_key[:4]
            print("gname", guest_name)
        else:
            # If session key doesn't exist (unlikely case), generate a random string
            guest_name = get_random_string(4)
            print(guest_name)

        # Set the author name to the guest name
        serializer.save(author_name="Guest-" + guest_name)


        
class LikeToggleView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)

        initial_session_key = request.session.session_key

        print(f"Session Key: {initial_session_key}")

        existing_like = Like.objects.filter(post=post, session_key=initial_session_key)
        if request.user.is_authenticated:
            existing_like = existing_like | Like.objects.filter(post=post, user=request.user)

        if existing_like.exists():
            existing_like.delete()
            post.likes_count -= 1
            post.save()
            return Response({
                'detail': 'Post unliked successfully.',
                'likes_count': post.likes_count,
                'is_liked': False,
                'session_key': initial_session_key 
            }, status=status.HTTP_200_OK)
        else:
            like = Like(post=post, session_key=initial_session_key)
            if request.user.is_authenticated:
                like.user = request.user
            like.save()
            post.likes_count += 1
            post.save()
            return Response({
                'detail': 'Post liked successfully.',
                'likes_count': post.likes_count,
                'is_liked': True,
                'session_key': initial_session_key 
            }, status=status.HTTP_201_CREATED)
        



class ProjectUserWritePermission(permissions.BasePermission):
    message = 'Editing projects is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    
class ProjectsList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
    
class ProjectDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class CreateProject(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AdminProjectDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

class EditProject(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, ProjectUserWritePermission]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class DeleteProject(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, ProjectUserWritePermission]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class TechnologyListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        technologies = Technology.objects.all()
        serializer = TechnologySerializer(technologies, many=True)
        return Response(serializer.data)

class PopularPostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Post.objects.filter(deleted=False, status='published').order_by('-likes_count')[:3]
    


    
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        