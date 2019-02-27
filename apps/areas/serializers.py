from rest_framework.serializers import ModelSerializer

from areas.models import Area
from users.models import Address


class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class SubAreaSerializer(ModelSerializer):
    """ 子行政区划信息序列化器 """
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')

