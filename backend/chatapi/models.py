from django.db import models

class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
