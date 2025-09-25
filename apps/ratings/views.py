from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import RatingCategory, SmartRating, Rating, RatingReport, RatingSettings, RatingStatistics
from .serializers import (
    RatingCategorySerializer, SmartRatingSerializer, RatingSerializer,
    RatingReportSerializer, RatingSettingsSerializer, RatingStatisticsSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class RatingCategoryViewSet(viewsets.ModelViewSet):
    queryset = RatingCategory.objects.all()
    serializer_class = RatingCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class SmartRatingViewSet(viewsets.ModelViewSet):
    queryset = SmartRating.objects.all()
    serializer_class = SmartRatingSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def set_initial_values(self, request, pk=None):
        smart_rating = get_object_or_404(SmartRating, pk=pk)
        # Logic to set initial fake_rating and fake_count
        return Response({"status": "initial values set"})

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Rating.objects.all()
        return Rating.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingReportViewSet(viewsets.ModelViewSet):
    queryset = RatingReport.objects.all()
    serializer_class = RatingReportSerializer
    permission_classes = [permissions.IsAdminUser]

class RatingSettingsViewSet(viewsets.ModelViewSet):
    queryset = RatingSettings.objects.all()
    serializer_class = RatingSettingsSerializer
    permission_classes = [permissions.IsAdminUser]

class RatingStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RatingStatistics.objects.all()
    serializer_class = RatingStatisticsSerializer
    permission_classes = [permissions.AllowAny]

