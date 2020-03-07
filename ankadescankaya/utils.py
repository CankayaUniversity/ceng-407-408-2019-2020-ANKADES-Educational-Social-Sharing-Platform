from django.utils.text import slugify


def unique_slug_generator(model_instance, title, slug_field):
    """
    :param model_instance:
    :param title:
    :param slug_field:
    :return:
    """
    slug = slugify(title)
    model_class = model_instance.__class__
    object_count = 0
    while model_class._default_manager.filter(slug=slug).exists():
        object_count += 1
        slug = f'{slug}-{object_count}'
    return slug