from django.urls import path

from .views import ClothingItemUploadView, RatingCreateView, RecommendOutfitView

urlpatterns = [
    path("items/upload/", ClothingItemUploadView.as_view(), name="clothing_upload"),
    path("recommend/", RecommendOutfitView.as_view(), name="recommend"),
    path("ratings/", RatingCreateView.as_view(), name="ratings"),
]
