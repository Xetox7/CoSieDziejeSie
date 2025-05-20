from django.contrib.auth.models import User
from django.db import models
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify


class Topic(models.Model):
    name = models.CharField(max_length=200, default="")
    slug = models.SlugField(max_length=200, default="")
    prepopulated_fields = {"slug": ("name",)}

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, default="")
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    description = tinymce_models.HTMLField(blank=True, default="")
    date = models.DateField(null=True)
    time = models.TimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    location = models.CharField(default="", max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name


class Meta:
    ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(default="")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
