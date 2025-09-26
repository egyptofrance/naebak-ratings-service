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
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

@extend_schema_view(
    list=extend_schema(summary="عرض جميع فئات التقييم", description="عرض قائمة بجميع فئات التقييم المتاحة في النظام."),
    retrieve=extend_schema(summary="عرض فئة تقييم محددة", description="عرض تفاصيل فئة تقييم محددة باستخدام المعرف الخاص بها."),
    create=extend_schema(summary="إنشاء فئة تقييم جديدة", description="إنشاء فئة تقييم جديدة. (يتطلب صلاحيات مسؤول)"),
    update=extend_schema(summary="تحديث فئة تقييم", description="تحديث بيانات فئة تقييم موجودة. (يتطلب صلاحيات مسؤول)"),
    partial_update=extend_schema(summary="تحديث جزئي لفئة تقييم", description="تحديث جزئي لبيانات فئة تقييم موجودة. (يتطلب صلاحيات مسؤول)"),
    destroy=extend_schema(summary="حذف فئة تقييم", description="حذف فئة تقييم موجودة. (يتطلب صلاحيات مسؤول)")
)
class RatingCategoryViewSet(viewsets.ModelViewSet):
    queryset = RatingCategory.objects.all()
    serializer_class = RatingCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

@extend_schema_view(
    list=extend_schema(summary="عرض جميع التقييمات الذكية", description="عرض قائمة بجميع التقييمات الذكية المتاحة في النظام."),
    retrieve=extend_schema(summary="عرض تقييم ذكي محدد", description="عرض تفاصيل تقييم ذكي محدد باستخدام المعرف الخاص به."),
    create=extend_schema(summary="إنشاء تقييم ذكي جديد", description="إنشاء تقييم ذكي جديد. (يتطلب صلاحيات مسؤول)"),
    update=extend_schema(summary="تحديث تقييم ذكي", description="تحديث بيانات تقييم ذكي موجود. (يتطلب صلاحيات مسؤول)"),
    partial_update=extend_schema(summary="تحديث جزئي لتقييم ذكي", description="تحديث جزئي لبيانات تقييم ذكي موجود. (يتطلب صلاحيات مسؤول)"),
    destroy=extend_schema(summary="حذف تقييم ذكي", description="حذف تقييم ذكي موجود. (يتطلب صلاحيات مسؤول)"),
    set_initial_values=extend_schema(summary="ضبط القيم الأولية للتقييم الذكي", description="ضبط القيم الأولية للتقييم الذكي (التقييم الوهمي وعدد التقييمات الوهمية). (يتطلب صلاحيات مسؤول)")
)
class SmartRatingViewSet(viewsets.ModelViewSet):
    queryset = SmartRating.objects.all()
    serializer_class = SmartRatingSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def set_initial_values(self, request, pk=None):
        smart_rating = get_object_or_404(SmartRating, pk=pk)
        # Logic to set initial fake_rating and fake_count
        return Response({"status": "initial values set"})

@extend_schema_view(
    list=extend_schema(summary="عرض التقييمات", description="عرض قائمة بالتقييمات. يمكن للمستخدمين العاديين رؤية تقييماتهم فقط، بينما يمكن للمسؤولين رؤية جميع التقييمات."),
    retrieve=extend_schema(summary="عرض تقييم محدد", description="عرض تفاصيل تقييم محدد."),
    create=extend_schema(summary="إنشاء تقييم جديد", description="إنشاء تقييم جديد. يتم ربط التقييم تلقائياً بالمستخدم الحالي."),
    update=extend_schema(summary="تحديث تقييم", description="تحديث بيانات تقييم موجود."),
    partial_update=extend_schema(summary="تحديث جزئي لتقييم", description="تحديث جزئي لبيانات تقييم موجود."),
    destroy=extend_schema(summary="حذف تقييم", description="حذف تقييم موجود.")
)
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

