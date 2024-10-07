from rest_framework import filters
from .models import UserHabit


class HabitFilter(filters.BaseFilterBackend):
    """
    Filter out only objects that belong to a specific User.
    """

    def filter_queryset(self, request, queryset, view):
        user_habits = UserHabit.objects.filter(user=request.user).values_list('habit', flat=True)

        queryset = queryset.exclude(id__in=user_habits)

        return queryset
