from goods.models import Goods

from rest_framework import serializers


class CartGoodserislizer(serializers.ModelSerializer):
    count = serializers.IntegerField(label='商品數量', read_only=True)
    selected = serializers.BooleanField(label='是否勾選', read_only=True)

    class Meta:
        model = Goods
        fields = ('id', 'sell_price', 'img_url', 'title', 'count', 'selected')


class CarAddSerislizer(serializers.Serializer):
    good_id = serializers.IntegerField(label='商品id')
    count = serializers.IntegerField(label='商品數量')


class CarPutSerislizer(serializers.Serializer):
    good_id = serializers.IntegerField(label='商品id', read_only=True)
    count = serializers.IntegerField(label='商品數量', read_only=True)
    selected = serializers.BooleanField(label='是否勾選', read_only=True)


class CarDeleteSerislizer(serializers.Serializer):
    gooo_id = serializers.IntegerField(label='商品ID')


class CarCountSerislizer(serializers.Serializer):
    counts = serializers.IntegerField(label='商品數量')


class CartSelectedAllSerislizer(serializers.Serializer):
    selected = serializers.BooleanField(label='是否勾選')
