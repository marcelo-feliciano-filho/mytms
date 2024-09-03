from rest_framework import viewsets
from .models import Campaign, Member, Task
from .serializers import CampaignSerializer, MemberSerializer, TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Prefetch


class CampaignViewSet(viewsets.ModelViewSet):
    """
    CampaignViewSet -> has the queryset with all objects and the proper serializer class for Campaign model.
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class MemberViewSet(viewsets.ModelViewSet):
    """
    MemberViewSet -> has the queryset with all objects and the proper serializer class for Member model.
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    TaskViewSet -> has the queryset with selected objects and the proper serializer class with a filter and a paginated
    view for custom queryset.
    """
    queryset = Task.objects.select_related('campaign', 'trainer', 'lead')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination

    @action(detail=False, methods=["Get"])
    def tasks_by_week(self, request, tasks_per_page=25):
        week_number = request.query_params.get("week", timezone.now().isocalendar()[1])
        tasks = Task.objects.filter(
            created_at__week=week_number
        ).select_related('campaign', 'trainer', 'lead').prefetch_related(
            Prefetch("trainer__campaigns", queryset=Campaign.objects.all())
        ).order_by("created_at")[:tasks_per_page]
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
