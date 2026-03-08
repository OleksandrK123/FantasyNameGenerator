from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class NameCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class FantasyName(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(NameCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FavoriteName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50, blank=True)
    added_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.race})"