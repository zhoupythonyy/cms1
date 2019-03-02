from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from goods import serializers
from goods.models import Goods, GoodsCategory


class DetailView(APIView):
    """商品详情"""
    def get(self, request, goods_id):
        try:
            goods = Goods.objects.get(id=goods_id)
        except Goods.DoesNotExist:
            raise ValidationError("商品不存在")
        goodsalbum_set = goods.goodsalbum_set.all()
        goods = serializers.GoodsSerializers(goods).data

        category = serializers.SCategorySer(GoodsCategory.objects.get(id=goods['category'])).data
        category['parent'] = serializers.SCategorySer(GoodsCategory.objects.get(id=goods['category']).parent).data
        goods['category'] = category
        goods['goodsalbum_set'] = serializers.GoodsAlbumSer(goodsalbum_set, many=True).data
        return Response(goods)


class RecommendView(ListAPIView):
    """获取推荐商品"""
    queryset = Goods.objects.filter(is_red=1).order_by('-create_time')[0:4]
    serializer_class = serializers.GoodsSerializers
