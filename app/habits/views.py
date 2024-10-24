import copy

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Habit,
    UserHabit,
    HabitLog,
)
from .serializers import (
    HabitSerializer,
    UserHabitSerializer,
    UserHabitRetrieveSerializer,
    HabitLogSerializer,
)
from app.users.filters import UserFilter
from .filters import HabitFilter


class HabitViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    queryset = Habit.objects.all()
    list_filter_classes = [
        SearchFilter,
    ]
    permission_classes = [IsAuthenticated]

    def get_filter_backends(self):
        if self.action == 'list':
            extra_filters = self.list_filter_classes
        else:
            extra_filters = []

        return [*extra_filters, HabitFilter]

    def get_serializer_class(self):
        return HabitSerializer

    def generate_serializer_data(self, request):
        serializer_data = copy.copy(request.data)

        return serializer_data


class UserHabitViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = UserHabit.objects.all()
    list_filter_classes = [
        SearchFilter,
    ]
    permission_classes = [IsAuthenticated]

    def get_filter_backends(self):
        if self.action == 'list':
            extra_filters = self.list_filter_classes
        else:
            extra_filters = []

        return [*extra_filters, UserFilter]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserHabitRetrieveSerializer
        return UserHabitSerializer

    def generate_serializer_data(self, request):
        serializer_data = copy.copy(request.data)
        return serializer_data

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        habit_log = HabitLog.objects.filter(
            user=request.user,
            habit=response.data['habit']['id']
        ).order_by('-created_at')
        response.data['habitLogs'] = HabitLogSerializer(habit_log, many=True).data
        return Response(response.data, status=status.HTTP_200_OK)
