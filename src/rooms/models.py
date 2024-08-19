from cgitb import text
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from django.utils.translation import gettext as _

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("rooms-topic", kwargs={"pk": self.pk})


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("rooms-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-updated", "-created"]


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.text[:50]

    def get_absolute_url(self):
        return reverse("message-delete", kwargs={"pk": self.room.pk, "id": self.id})
