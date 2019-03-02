from rest_framework import serializers

from goods.models import Goods, GoodsAlbum, GoodsCategory


class GoodsSerializers(serializers.ModelSerializer):
    """推荐商品序列化器"""
    class Meta:
        model = Goods
        fields = '__all__'


class GoodsAlbumSer(serializers.ModelSerializer):
    class Meta:
        model = GoodsAlbum
        fields = '__all__'


class SCategorySer(serializers.ModelSerializer):
    """商品类别"""
    class Meta:
        model = GoodsCategory
        fields = ('id', 'title')
