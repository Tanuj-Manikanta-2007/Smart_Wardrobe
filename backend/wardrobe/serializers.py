from __future__ import annotations

from rest_framework import serializers

from .models import ClothingItem, Rating


class ClothingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothingItem
        fields = [
            "id",
            "image",
            "clothing_type",
            "color",
            "feature_vector",
            "created_at",
        ]
        read_only_fields = ["id", "feature_vector", "created_at"]


class ClothingItemUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothingItem
        fields = ["id", "image", "clothing_type", "color", "created_at"]
        read_only_fields = ["id", "created_at"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "outfit_id", "rating", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_rating(self, value: int) -> int:
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
