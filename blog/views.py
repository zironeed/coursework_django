from django.views.generic import DetailView
from blog.models import Blog


class BlogCard(DetailView):
    """Information about blog."""
    model = Blog
    template_name = "blog/blog_card.html"
    slug_url_kwarg = "blog_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.get_object()
        context["Title"] = current_object.title
        context["Blog"] = current_object
        current_object.views += 1
        current_object.save()
        return context
