from django.contrib import admin
from .models import NameCategory, FantasyName, FavoriteName

# Register your models here.


@admin.register(NameCategory)
class NameCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FantasyName)
class FantasyNameAdmin(admin.ModelAdmin):
    # What columns to show in the list
    list_display = ('name', 'category', 'created_at')
    # Filter sidebar on the right
    list_filter = ('category', 'created_at')
    # Search box at the top
    search_fields = ('name',)
    # Date hierarchy for easy navigation by timeline
    date_hierarchy = 'created_at'

@admin.register(FavoriteName)
class FavoriteNameAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'race', 'added_at')
    list_filter = ('race', 'added_at', 'user')
    search_fields = ('name', 'user__username')
    # Make sure 'added_at' is read-only if it's set automatically
    readonly_fields = ('added_at',)
