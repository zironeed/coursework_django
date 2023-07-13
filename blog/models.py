from django.db import models


class Blog(models.Model):
    """Model for blog"""
    title = models.CharField(max_length=100, verbose_name="blog title", null=False, blank=False, unique=True)
    plot = models.TextField(max_length=500, null=False, blank=False, verbose_name="blog description")
    image = models.ImageField(upload_to="images", null=True, blank=True)
    views = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=255, verbose_name="blog slug", null=False, unique=True)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ["date", "title"]

    def __str__(self):
        return self.title
