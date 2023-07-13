from django.core.cache import cache

from config import settings
from mailing.models import Blog


def get_cached_for_blog_list():
    '''Кэширование списка блогов'''
    if settings.CACHE_ENABLED:
        key = f'blog_list'
        object_list = cache.get(key)
        if object_list is None:
            object_list = Blog.objects.all()
            cache.set(key, object_list)
    else:
        object_list = Blog.objects.all()

    return object_list
