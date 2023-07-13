from django.urls import path
from blog.views import BlogCard
from django.views.decorators.cache import cache_page


app_name = "blog"

urlpatterns = [
    path("blog_card/<int:pk>", cache_page(60)(BlogCard.as_view()), name="blog_card"),
]
