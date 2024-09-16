import copy

from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
)

import logging

logger = logging.getLogger(__name__)


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = User.objects.all()
    account_lookup_kwarg = 'account_pk'
    list_filter_classes = [
        SearchFilter,
    ]

    @property
    def filter_backends(self):
        if self.action == 'list':
            extra_filters = self.list_filter_classes
        else:
            extra_filters = []

        return [*extra_filters]

    def get_permissions(self):
        if self.action in ['create', 'test']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def generate_serializer_data(self, request):
        serializer_data = copy.copy(request.data)

        return serializer_data

    def create(self, request):
        serializer_data = self.generate_serializer_data(request)
        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user_serializer = UserSerializer(user)

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='me', suffix='me')
    def me(self, request):
        serializer_data = UserSerializer(request.user)

        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='test', suffix='test')
    def test(self, request):
        return Response('No Autentication Required', status=status.HTTP_200_OK)
