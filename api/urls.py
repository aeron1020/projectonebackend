from django.urls import path
from .views import CategoryList, PostList, PostDetail, ProjectDetails, CreatePost, AdminPostDetails, EditPost, DeletePost, PostListDetailFilter, UserPostsList, CreateComment, PostCommentsList, UserDetailView, CreateCommentForGuest, LikeToggleView, ProjectsList, CreateProject, AdminProjectDetails, EditProject, DeleteProject, TechnologyListView, PopularPostList, PasswordChangeView

app_name = 'personal_portfolio'

urlpatterns = [

    path('', PostList.as_view(), name='post-list'),
    path('posts/<slug>/', PostDetail.as_view(), name='post-detail'),
    path('search/', PostListDetailFilter.as_view(), name='postsearch'),
    path('user/posts/', UserPostsList.as_view(), name='user-post-list'),

    path('admin/create/', CreatePost.as_view(), name='create-post'),
    path('admin/edit/post-detail/<int:pk>/', AdminPostDetails.as_view(), name='admin-post-detail'),
    path('admin/edit-post/<int:pk>/', EditPost.as_view(), name='edit-post'),
    path('admin/delete-post/<int:pk>/', DeletePost.as_view(), name='delete-post'),

    path('posts/<int:pk>/comments/create/', CreateComment.as_view(), name='create-comment'),
    path('posts/<int:pk>/comments/create/guest/', CreateCommentForGuest.as_view(), name='create-comment-guest'),
    path('posts/<int:pk>/comments/', PostCommentsList.as_view(), name='post-comments-list'),

    path('posts/<int:pk>/like/', LikeToggleView.as_view(), name='like_toggle'),

    path('user/', UserDetailView.as_view(), name='user-detail'),

    path('password-change/', PasswordChangeView.as_view(), name='password_change'),

    path('categories/', CategoryList.as_view(), name='category-list'),
    path('technologies/', TechnologyListView.as_view(), name='technology-list'),
    path('popular-posts/', PopularPostList.as_view(), name='popular-posts'),

    path('admin/projects/', ProjectsList.as_view(), name='projects'),
    path('admin/project/<int:pk>/', ProjectDetails.as_view(), name='admin-project-detail'),
    path('admin/create_project/', CreateProject.as_view(), name='create-project'),
    path('admin/edit/project-detail/<int:pk>/', AdminProjectDetails.as_view(), name='admin-project-detail'),
    path('admin/edit-project/<int:pk>/', EditProject.as_view(), name='edit-project'),
    path('admin/delete-project/<int:pk>/', DeleteProject.as_view(), name='delete-project'),



]





