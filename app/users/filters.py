from rest_framework import filters


class UserFilter(filters.BaseFilterBackend):
    """
    Filter out only objects that belong to a specific User.
    """

    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(user=request.user)

        return queryset
