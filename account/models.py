import uuid
from ckeditor.fields import RichTextField
# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = RichTextField(verbose_name="Description", null=True, blank=True)
    image = models.FileField(blank=True, default='default-user-image.png', null=True,)

    def __str__(self):
        return self.username
