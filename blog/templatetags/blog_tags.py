from django import template
from ..models import Post
from django.contrib.auth.models import User
from django.db.models import Count

register = template.Library()


@register.simple_tag
def prolific_users():
    return User.objects.annotate(p_users=Count('posts')).order_by('-p_users')[:3]


