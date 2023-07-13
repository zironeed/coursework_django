from django import template
register = template.Library()


@register.simple_tag(name="media_path")
def get_image_path(image_path):
    return f"/media/{image_path}"
