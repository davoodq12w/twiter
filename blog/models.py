from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django_resized import ResizedImageField


# Create your models here.

class Post(models.Model):
    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    class Status(models.TextChoices):
        DRAFT = ("draft", "Draft")
        REJECTED = ("rejected", "Rejected")
        PUBLISHED = ("published", "Published")

    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.CharField(max_length=250)

    publish = models.DateTimeField(default=timezone.now)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    status = models.CharField(max_length=250, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.id])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    status = models.BooleanField(default=False)
    auther = models.CharField(max_length=250)
    text = models.TextField(max_length=500)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['create']
        indexes = [
            models.Index(fields=['create'])
        ]

    def __str__(self):
        return self.auther


def image_sorter(instance, filename):
    return f"post_images/{instance.create.year}/{filename}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    create = models.DateTimeField(auto_now_add=True)
    image = ResizedImageField(upload_to=image_sorter, quality=70)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['create']
        indexes = [
            models.Index(fields=['create'])
        ]

    def __str__(self):
        if self.title:
            return self.title
        else:
            self.title = self.image.name
            return self.title


