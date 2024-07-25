from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    # model manager 
    # by default we want to return the data from the database and only display the posts that are status is published so this custom manager is created.
    # if instead of running objects all on the data when we make a query  we can run this PostObjects so we can utilize this filter by default to collect all the data that has the status of published.
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published', deleted=False)
        

    options = (('draft', 'Draft'), 
               ('published', 'Published')) # for the status

    category = models.ForeignKey("Category", on_delete=models.PROTECT, default=1)
    head_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    content = models.TextField(default="Default Content")
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=options, default='published')
    # Add deleted flag
    deleted = models.BooleanField(default=False)
    # like counts
    likes_count = models.PositiveIntegerField(default=0)

    def user_has_liked(self, user):
        if user.is_authenticated:
            return Like.objects.filter(post=self, user=user).exists()
        return False
    
    # default manager
    objects = models.Manager()
    # custom manager
    postobjects = PostObjects()

    class Meta:
        # return the data in decending order
        ordering = ('-published',)

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    content = models.TextField()
    author_name = models.CharField(max_length=100, default='Anonymous')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(default=timezone.now)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=False, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['post', 'user', 'session_key']

    def __str__(self):
        if self.user:
            return f'{self.user.user_name} likes {self.post.title}'
        return f'Session {self.session_key} likes {self.post.title}'
    

class Technology(models.Model):
    name = models.CharField(max_length=100)
    logoUrl = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    project_title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    tech_stack = models.ManyToManyField('Technology', related_name='projects', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.project_title
    
    
    