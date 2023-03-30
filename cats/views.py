from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.throttling import AnonRateThrottle

from .models import Achievement, Cat, User
from .pagination import CatsPagination
from .permissions import OwnerOrReadOnly, ReadOnly

from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .throttling import WorkingHoursRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (AnonRateThrottle, WorkingHoursRateThrottle)
    pagination_class = None  # CatsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name', 'id')
    ordering_fields = ('name', 'birth_year', 'id')  # Or "__all__'
    ordering = ('birth_year',)  # Сортировка по умолчанию
    # throttle_scope = 'low_request'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return ReadOnly(),
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
