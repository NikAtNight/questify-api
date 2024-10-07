import copy

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Habit, UserHabit
from .serializers import (
    HabitSerializer,
    UserHabitSerializer
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

    @property
    def filter_backends(self):
        if self.action == 'list':
            extra_filters = self.list_filter_classes
        else:
            extra_filters = []

        return [*extra_filters, HabitFilter]

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_serializer_class(self):
        return HabitSerializer

    def generate_serializer_data(self, request):
        serializer_data = copy.copy(request.data)

        return serializer_data


class UserHabitViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    queryset = UserHabit.objects.all()
    list_filter_classes = [
        SearchFilter,
    ]

    @property
    def filter_backends(self):
        if self.action == 'list':
            extra_filters = self.list_filter_classes
        else:
            extra_filters = []

        return [*extra_filters, UserFilter]

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_serializer_class(self):
        return UserHabitSerializer

    def generate_serializer_data(self, request):
        serializer_data = copy.copy(request.data)

        return serializer_data
