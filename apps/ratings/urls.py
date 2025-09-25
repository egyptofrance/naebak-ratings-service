from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RatingCategoryViewSet, SmartRatingViewSet, RatingViewSet,
    RatingReportViewSet, RatingSettingsViewSet, RatingStatisticsViewSet
)

router = DefaultRouter()
router.register(r'categories', RatingCategoryViewSet)
router.register(r'smart-ratings', SmartRatingViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'reports', RatingReportViewSet)
router.register(r'settings', RatingSettingsViewSet)
router.register(r'statistics', RatingStatisticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

