from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from main import serializers
from main.models import Advert, City


class AdminCityViewset(viewsets.ModelViewSet):
    """Вьюха для управления городами администратором."""
    permission_classes = [IsAdminUser]
    queryset = City.objects.all()
    serializer_class = serializers.CitySerializer


class UserAdvertViewset(viewsets.ModelViewSet):
    """Вьюха для управления объявлениями пользователем сайта."""
    permission_classes = [IsAuthenticated]
    queryset = Advert.objects.all()
    serializer_class = serializers.UserAdvertSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = serializers.AdvertDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class AdvertDetailApiView(RetrieveAPIView):
    """Вывод объявления."""
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertDetailSerializer


class AdvertListApiView(ListAPIView):
    """Вывод списка объявлений. Поддерживает поиск, сортировка, фильтр.
    Для этого принимает аргументы в запросе
    city=1&user=1 отфильтровать объявления по конкретному пользователю и городу
    sort= 1 | -1  сортировка по дате добавления
    search=поиск  поиск по тексту объявления
    """
    queryset = Advert.objects.all()
    serializer_class = serializers.AdvertDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'user']

    def get_queryset(self):
        param = self.request.query_params
        qs = super().get_queryset()

        search = param.get('search')
        if search:
            qs = qs.search_by_body(search)

        sort = param.get('sort')
        if sort == "1":
            qs = qs.order_by('created')
        elif sort == "-1":
            qs = qs.order_by('-created')

        return qs
