from __future__ import annotations

import requests
from django.conf import settings

from ..models import ClothingItem, MLTrainingEvent, Rating


class MLServiceError(RuntimeError):
    pass


def _post_json(path: str, payload: dict) -> dict:
    base_url = settings.ML_SERVICE_URL.rstrip("/")
    url = f"{base_url}/{path.lstrip('/')}"
    try:
        resp = requests.post(url, json=payload, timeout=15)
    except requests.RequestException as exc:
        raise MLServiceError(str(exc)) from exc

    if resp.status_code >= 400:
        raise MLServiceError(f"ML service error {resp.status_code}: {resp.text}")

    try:
        return resp.json()
    except ValueError as exc:
        raise MLServiceError("ML service did not return JSON") from exc


def recommend_for_user(*, user_id: int) -> dict:
    return _post_json("recommend", {"user_id": user_id})


def trigger_training() -> dict:
    return _post_json("train", {})


def store_feature_vectors_from_ml_response(ml_response: dict) -> int:
    """If ML returns item feature vectors, persist them on ClothingItem.

    Expected shape:
      {
        "item_feature_vectors": {
          "12": [0.1, 0.2, ...],
          "13": [0.3, 0.4, ...]
        }
      }
    """
    vectors = ml_response.get("item_feature_vectors")
    if not isinstance(vectors, dict):
        return 0

    updated = 0
    for item_id_str, vector in vectors.items():
        try:
            item_id = int(item_id_str)
        except (TypeError, ValueError):
            continue
        ClothingItem.objects.filter(id=item_id).update(feature_vector=vector)
        updated += 1

    return updated


def maybe_trigger_retraining(*, triggered_by_user) -> dict | None:
    """Trigger ML retraining if ratings since last training >= threshold.

    Returns ML response if training was triggered, else None.
    """
    threshold = getattr(settings, "ML_RETRAIN_RATINGS_THRESHOLD", 50)
    last_event = MLTrainingEvent.objects.order_by("-created_at").first()
    ratings_qs = Rating.objects.all()
    if last_event is not None:
        ratings_qs = ratings_qs.filter(created_at__gt=last_event.created_at)

    new_ratings = ratings_qs.count()
    if new_ratings < threshold:
        return None

    try:
        ml_resp = trigger_training()
    except MLServiceError as exc:
        MLTrainingEvent.objects.create(triggered_by_user=triggered_by_user, status=MLTrainingEvent.STATUS_FAILED, response={"error": str(exc)})
        return None

    MLTrainingEvent.objects.create(triggered_by_user=triggered_by_user, status=MLTrainingEvent.STATUS_TRIGGERED, response=ml_resp)
    return ml_resp
