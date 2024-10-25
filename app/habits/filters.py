from rest_framework import filters
from .models import UserHabit
from app.core.enums import HabitStatusEnum
from django.db.models import Q


class HabitFilter(filters.BaseFilterBackend):
    """
    Filter out only objects that belong to a specific User.
    """

    def filter_queryset(self, request, queryset, view):
        user_habits = UserHabit.objects.filter(user=request.user)

        # Exclude user habits that are not abandoned
        queryset = queryset.exclude(
            Q(id__in=user_habits.exclude(status=HabitStatusEnum.ABANDONED.name).values_list('habit', flat=True))
        )

        return queryset


class UserHabitFilter(filters.BaseFilterBackend):
    """
    Filter out only objects that belong to a specific User.
    """

    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(user=request.user)

        queryset = queryset.exclude(status=HabitStatusEnum.ABANDONED.name)

        return queryset
