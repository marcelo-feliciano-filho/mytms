from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..tms_manager.views import CampaignViewSet, MemberViewSet, TaskViewSet

router = DefaultRouter()
router.register(r"campaigns", CampaignViewSet)
router.register(r"members", MemberViewSet)
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("tms_manager/admin/", admin.site.urls),
    path("/api", include(router.urls))
]
