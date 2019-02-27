from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from areas.models import Area
from areas.serializers import AreaSerializer, SubAreaSerializer


class AreaProvinceView(ListAPIView):
    queryset = Area.objects.filter(parent=None)
    serializer_class = AreaSerializer
    pagination_class = None


class SubAreaView(RetrieveAPIView):
    queryset = Area.objects.all()
    serializer_class = SubAreaSerializer
