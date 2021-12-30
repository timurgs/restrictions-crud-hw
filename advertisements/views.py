from django.contrib.auth.models import User
from django_filters import DateFromToRangeFilter, FilterSet, ModelChoiceFilter, ChoiceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer


class FilterDate(FilterSet):
    created_at = DateFromToRangeFilter()
    updated_at = DateFromToRangeFilter()
    creator = ModelChoiceFilter(queryset=User.objects.all())
    status = ChoiceFilter(choices=AdvertisementStatusChoices.choices)

    class Meta:
        model = Advertisement
        fields = ['created_at', 'updated_at', 'creator', 'status']


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterDate

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return []
