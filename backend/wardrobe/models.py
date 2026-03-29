from __future__ import annotations

from django.conf import settings
from django.db import models


class ClothingItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clothing_items")
    image = models.ImageField(upload_to="clothes/")
    clothing_type = models.CharField(max_length=64, blank=True)
    color = models.CharField(max_length=32, blank=True)
    feature_vector = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"ClothingItem(id={self.id}, user_id={self.user_id})"


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    outfit_id = models.IntegerField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Rating(id={self.id}, user_id={self.user_id}, outfit_id={self.outfit_id}, rating={self.rating})"


class MLTrainingEvent(models.Model):
    STATUS_TRIGGERED = "triggered"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_TRIGGERED, "Triggered"),
        (STATUS_FAILED, "Failed"),
    ]

    triggered_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ml_training_events",
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"MLTrainingEvent(id={self.id}, status={self.status})"
