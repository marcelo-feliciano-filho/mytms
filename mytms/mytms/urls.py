from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("tms_manager/admin/", admin.site.urls),
]
