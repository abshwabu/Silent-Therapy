from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, username, password=None, **extra_fields):
        """Create a new user."""
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """Create a new superuser."""
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

class Patient(models.Model):
    """Patient object."""
    condition = models.CharField(max_length=255)
    special_request = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

class ChatBot(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text_input = models.CharField(max_length=500)
    gemini_output = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.text_input


class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")
    current_users = models.ManyToManyField(User, related_name="current_rooms", blank=True)

    def __str__(self):
        return f"Room({self.name} {self.host})"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.room})"
