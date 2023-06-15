from django import template
from random import randint
from news.models import Post

register = template.Library()


@register.simple_tag()
def random_new_id():
    return randint(1, len(Post.objects.all()))


