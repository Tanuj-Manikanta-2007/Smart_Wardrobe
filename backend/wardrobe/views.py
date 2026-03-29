from __future__ import annotations

from rest_framework import generics, parsers, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ClothingItemUploadSerializer, RatingSerializer
from .services.ml import MLServiceError, maybe_trigger_retraining, recommend_for_user, store_feature_vectors_from_ml_response


class ClothingItemUploadView(generics.CreateAPIView):
    serializer_class = ClothingItemUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecommendOutfitView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            ml_response = recommend_for_user(user_id=request.user.id)
        except MLServiceError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        store_feature_vectors_from_ml_response(ml_response)
        return Response(ml_response)


class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        maybe_trigger_retraining(triggered_by_user=self.request.user)
