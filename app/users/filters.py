from rest_framework import filters

from app.core.enums import HabitStatusEnum


class UserFilter(filters.BaseFilterBackend):
    """
    Filter out only objects that belong to a specific User.
    """

    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(user=request.user).exclude(status=HabitStatusEnum.ABANDONED)

        return queryset
