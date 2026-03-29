from django.contrib import admin

from .models import ClothingItem, MLTrainingEvent, Rating


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "clothing_type", "color", "created_at")
    list_filter = ("clothing_type", "color", "created_at")
    search_fields = ("user__username", "user__email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "outfit_id", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "user__email")


@admin.register(MLTrainingEvent)
class MLTrainingEventAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "triggered_by_user", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("triggered_by_user__username", "triggered_by_user__email")
