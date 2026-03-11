from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class NameCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class FantasyName(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        NameCategory,
        on_delete=models.CASCADE,
        related_name='names'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fantasy Name"
        verbose_name_plural = "Fantasy Names"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class FavoriteName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50, blank=True)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'name')
        verbose_name = "Favorite Name"
        verbose_name_plural = "Favorite Names"

    def __str__(self):
        return f"{self.name} ({self.race})"