from django.db import models
from django.contrib.auth.models import AbstractUser
class Users(AbstractUser):
    email = models.EmailField(unique=True)
    # username, password already included in AbstractUser
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Or use make_password for secure hashes

    def __str__(self):
        return self.username
class Subscription(models.Model):
    SUBSCRIPTION_TYPES = (
        ('Free', 'Free'),
        ('Premium', 'Premium'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='Free')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20)  # 'user' or 'assistant'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file_url = models.URLField()
    file_type = models.CharField(max_length=100)  # e.g., image/jpeg