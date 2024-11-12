import copy

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from django.utils import timezone

from .models import (
    Habit,
    UserHabit,
    HabitLog,
)
from .serializers import (
    HabitSerializer,
    UserHabitSerializer,
    UserHabitCreateSerializer,
    UserHabitRetrieveSerializer,
    UserHabitUpdateSerializer,
    HabitLogSerializer,
    HabitLogCreateSerializer,
    MilestoneSerializer,
)
from .filters import HabitFilter, UserHabitFilter


class HabitViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    queryset = Habit.objects.all()
    list_filter_classes = [
        SearchFilter,
    ]
    permission_classes = [IsAuthenticated]

    @property
    def filter_backends(self):
        if self.action == 'list':
            extra_filters = self.list_filter_classes
        else:
            extra_filters = []

        return [HabitFilter, *extra_filters]

    def get_serializer_class(self):
        return HabitSerializer

    def generate_serializer_data(self, request):
        serializer_data = copy.copy(request.data)

        return serializer_data

    @action(detail=True, methods=['get'], url_path='milestones', suffix='milestones')
    def get_milestones(self, request, pk=None):
        habit = self.get_object()
        milestones = habit.milestones.all().order_by('day')
        serializer = MilestoneSerializer(milestones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserHabitViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = UserHabit.objects.prefetch_related('habit__milestones')
    list_filter_classes = [
        SearchFilter,
    ]
    permission_classes = [IsAuthenticated]

    @property
    def filter_backends(self):
        if self.action == 'list':
            extra_filters = self.list_filter_classes
        else:
            extra_filters = []

        return [UserHabitFilter, *extra_filters]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserHabitCreateSerializer
        elif self.action == 'retrieve':
            return UserHabitRetrieveSerializer
        elif self.action == 'update':
            return UserHabitUpdateSerializer
        return UserHabitSerializer

    def generate_serializer_data(self, request):
        serializer_data = copy.copy(request.data)
        return serializer_data

    def create(self, request, *args, **kwargs):
        serializer_data = self.generate_serializer_data(request)
        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer_data = self.generate_serializer_data(request)
        serializer = self.get_serializer(instance, data=serializer_data, partial=partial)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        updated_instance_serializer = UserHabitSerializer(instance)

        return Response(updated_instance_serializer.data, status=status.HTTP_200_OK)


class HabitLogViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = HabitLog.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        habitId = self.request.query_params.get('habitId')

        if month and year:
            try:
                start_date = timezone.make_aware(
                    timezone.datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
                )
                end_date = timezone.make_aware(
                    (start_date.replace(tzinfo=None) + timezone.timedelta(days=31)).replace(day=1)
                )
                queryset = queryset.filter(
                    user=user,
                    created_at__gte=start_date,
                    created_at__lt=end_date,
                    habit__id=habitId
                )
            except ValueError:
                pass

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return HabitLogCreateSerializer
        return HabitLogSerializer

    def generate_serializer_data(self, request):
        serializer_data = copy.copy(request.data)

        try:
            user = request.user
            serializer_data['user'] = user.pk
            timezone = request.headers.get('X-Timezone', 'UTC')
            serializer_data['timezone'] = timezone
        except Exception:
            pass

        return serializer_data

    def create(self, request, *args, **kwargs):
        serializer_data = self.generate_serializer_data(request)
        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(status=status.HTTP_200_OK)
