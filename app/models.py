from email.policy import default
from enum import unique
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User 

# Create your models here.
class WebsiteMeta(models.Model):
    """Model definition for WebsiteMeta."""

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    about = models.TextField()

    class Meta:
        """Meta definition for WebsiteMeta."""

        verbose_name = 'WebsiteMeta'
        verbose_name_plural = 'WebsiteMetas'

    def __str__(self):
        """Unicode representation of WebsiteMeta."""
        return self.title



class Profile(models.Model):
    """Model definition for Profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=200)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return self.user.first_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)


class Subscribe(models.Model):
    """Model definition for Subscribe."""

    email = models.EmailField(max_length=254, unique=True)
    date = models.DateField(auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for Subscribe."""

        verbose_name = 'Subscribe'
        verbose_name_plural = 'Subscribes'

    def __str__(self):
        """Unicode representation of Subscribe."""
        return self.email


class Tag(models.Model):
    """Model definition for Tag."""

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        """Meta definition for Tag."""

        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    """Model definition for Post."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/", height_field=None, width_field=None, max_length=None)
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='post')
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """Meta definition for Post."""

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Unicode representation of Post."""
        return f"{self.title}, last updated on {self.last_updated}."


class Comment(models.Model):
    """Model definition for Comment."""

    content = models.TextField()
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    website = models.CharField(max_length=200, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')

    class Meta:
        """Meta definition for Comment."""

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.name


