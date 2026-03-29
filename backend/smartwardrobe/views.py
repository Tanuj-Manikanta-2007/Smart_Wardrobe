from __future__ import annotations

from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


def home_page(request):
    return render(request, "index.html")


class ApiIndexView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            {
                "name": "SmartWardrobe API",
                "status": "ok",
                "endpoints": {
                    "home": "/",
                    "admin": "/admin/",
                    "register": "/api/accounts/register/",
                    "token": "/api/token/",
                    "token_refresh": "/api/token/refresh/",
                    "upload_item": "/api/wardrobe/items/upload/",
                    "recommend": "/api/wardrobe/recommend/",
                    "rate": "/api/wardrobe/ratings/",
                },
            }
        )
