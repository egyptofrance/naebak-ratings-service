from rest_framework import viewsets, permissions, status
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
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
    Read-only access is allowed for any request, so GET, HEAD, or OPTIONS requests are always allowed.
    Write permissions are only allowed to users who are marked as staff.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

@extend_schema_view(
    list=extend_schema(summary="List all rating categories", description="View a list of all available rating categories in the system."),
    retrieve=extend_schema(summary="Retrieve a specific rating category", description="View the details of a specific rating category using its ID."),
    create=extend_schema(summary="Create a new rating category", description="Create a new rating category. (Requires admin privileges)"),
    update=extend_schema(summary="Update a rating category", description="Update the data of an existing rating category. (Requires admin privileges)"),
    partial_update=extend_schema(summary="Partially update a rating category", description="Partially update the data of an existing rating category. (Requires admin privileges)"),
    destroy=extend_schema(summary="Delete a rating category", description="Delete an existing rating category. (Requires admin privileges)")
)
class RatingCategoryViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing rating categories.

    This ViewSet provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    Only admin users can create, update, or delete rating categories. All users can view them.
    """
    queryset = RatingCategory.objects.all()
    serializer_class = RatingCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

@extend_schema_view(
    list=extend_schema(summary="List all smart ratings", description="View a list of all smart ratings available in the system."),
    retrieve=extend_schema(summary="Retrieve a specific smart rating", description="View the details of a specific smart rating using its ID."),
    create=extend_schema(summary="Create a new smart rating", description="Create a new smart rating. (Requires admin privileges)"),
    update=extend_schema(summary="Update a smart rating", description="Update the data of an existing smart rating. (Requires admin privileges)"),
    partial_update=extend_schema(summary="Partially update a smart rating", description="Partially update the data of an existing smart rating. (Requires admin privileges)"),
    destroy=extend_schema(summary="Delete a smart rating", description="Delete an existing smart rating. (Requires admin privileges)"),
    set_initial_values=extend_schema(summary="Set initial values for a smart rating", description="Set the initial values for a smart rating (fake rating and fake count). (Requires admin privileges)")
)
class SmartRatingViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing smart ratings.

    This ViewSet allows administrators to control the `SmartRating` model, which blends real and fake ratings.
    """
    queryset = SmartRating.objects.all()
    serializer_class = SmartRatingSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def set_initial_values(self, request, pk=None):
        """
        A custom action to set the initial `fake_rating` and `fake_count` for a smart rating.
        This is useful for seeding a new user with a baseline rating.
        """
        smart_rating = get_object_or_404(SmartRating, pk=pk)
        # In a real implementation, you would likely get these values from the request data
        # For example: smart_rating.fake_rating = request.data.get('fake_rating', 4.5)
        # smart_rating.fake_count = request.data.get('fake_count', 1000)
        smart_rating.save()
        return Response({"status": "initial values set"})

@extend_schema_view(
    list=extend_schema(summary="List ratings", description="View a list of ratings. Regular users can only see their own ratings, while admins can see all ratings."),
    retrieve=extend_schema(summary="Retrieve a specific rating", description="View the details of a specific rating."),
    create=extend_schema(summary="Create a new rating", description="Create a new rating. The rating is automatically associated with the current user."),
    update=extend_schema(summary="Update a rating", description="Update the data of an existing rating."),
    partial_update=extend_schema(summary="Partially update a rating", description="Partially update the data of an existing rating."),
    destroy=extend_schema(summary="Delete a rating", description="Delete an existing rating.")
)
class RatingViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating, viewing, and managing user ratings.

    This ViewSet ensures that users can only view and manage their own ratings, unless they are an admin.
    When a new rating is created, it is automatically associated with the authenticated user.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the ratings
        for the currently authenticated user.
        """
        if self.request.user.is_staff:
            return Rating.objects.all()
        return Rating.objects.filter(rater=self.request.user)

    def perform_create(self, serializer):
        """
        Associate the rating with the current user.
        """
        serializer.save(rater=self.request.user)

class RatingReportViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing reports on ratings.

    This is an admin-only ViewSet for reviewing and acting on reports of abusive or inappropriate ratings.
    """
    queryset = RatingReport.objects.all()
    serializer_class = RatingReportSerializer
    permission_classes = [permissions.IsAdminUser]

class RatingSettingsViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing the global rating settings.

    This is an admin-only ViewSet for configuring the behavior of the rating system.
    It operates on a singleton `RatingSettings` object.
    """
    queryset = RatingSettings.objects.all()
    serializer_class = RatingSettingsSerializer
    permission_classes = [permissions.IsAdminUser]

class RatingStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for viewing rating statistics.

    This ViewSet provides a read-only endpoint for accessing cached rating statistics.
    The statistics are calculated and updated periodically in the `RatingStatistics` model.
    """
    queryset = RatingStatistics.objects.all()
    serializer_class = RatingStatisticsSerializer
    permission_classes = [permissions.AllowAny]

