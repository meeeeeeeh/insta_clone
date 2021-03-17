from django.db import models
from django.contrib.auth.models import User
import uuid


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name='sender_room', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receive_room', on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
