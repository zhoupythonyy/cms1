from rest_framework.permissions import IsAuthenticated

from cart.serializers import CarAddSerislizer
from cart.serializers import CartSelectedAllSerislizer
from cart.serializers import CarPutSerislizer
from cart.serializers import CarDeleteSerislizer, CarCountSerislizer
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.serializers import CartGoodserislizer
from goods.models import Goods
from django_redis import get_redis_connection


class CartAddViem(APIView):

    permission_classes = [IsAuthenticated]

    def perform_authentication(self, request):
        """
        drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
        如果认证不通过,则会抛异常返回401状态码
        问题: 抛异常会导致视图无法执行
        解决: 捕获异常即可
        """
        try:
            super().perform_authentication(request)
        except Exception as e:
            print('perform_authentication: ', e)

    def get(self, request):
        # 顯示購物車中的商品
        user = request.user
        redis_conn = get_redis_connection('cart')  # 操作數據庫對象
        cart_data = redis_conn.hgetall('cart_%s' % user.id)  # 哈希存儲
        list_selected = redis_conn.smembers('cart_selected_%s' % user.id)  # 存儲方式set集合

        cart = {}
        for good_id, count in cart_data.items():
            cart[int(good_id)] = {
                'count': int(count),
                'selected': good_id in list_selected
            }
        goods = CartGoodserislizer(Goods.objects.filter(id__in=cart.keys()), many=True).data
        data_list = []
        for good in goods:
            good['count'] = cart[good['id']].get('count')
            good['selected'] = cart[good['id']].get('selected')
            amount = '%.2f' % (float(good['sell_price']) * good['count'])
            good['amount'] = amount
            data_list.append(good)
        return Response(data_list)

    def post(self, request):
        # 實現功能 將商品添加到購物車中
        user = request.user
        s = CarAddSerislizer(data=request.data)
        s.is_valid(raise_exception=True)  # 異常拋出
        good_id = s.validated_data.get('good_id')
        count = s.validated_data.get('count')
        redis_conn = get_redis_connection('cart')
        p1 = redis_conn.pipeline()

        p1.hincrby('cart_%s' % user.id, good_id, count)
        p1.execute()
        return Response(s.data, status=201)

    def put(self, request):
        # 修改購物車信息 是否勾選，修改數量
        user = request.user

        # 用戶已經登陸
        serializer = CarPutSerislizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # good_id = serializer.validated_data.get('goods_id')
        good_id = request.data['goods_id']
        # count = serializer.validated_data.get('count')
        count = request.data['count']
        redis_coon = get_redis_connection('cart')
        p1 = redis_coon.pipeline()
        # 修改redis數據庫內容
        p1.hset('cart_%s' % user.id, good_id, count)
        p1.execute()
        data = {
            'count': count
        }
        return Response(data)

    def delete(self, request):
        user = request.user
        # 已經登入
        goods_id = request.data['goods_id']
        redis_conn = get_redis_connection('cart')
        p1 = redis_conn.pipeline()
        p1.hdel('cart_%s' % user.id, goods_id)
        p1.execute()
        return Response(status=200)


class CartCountView(APIView):
    """显示购物车的数量"""
    permission_classes = [IsAuthenticated]

    def perform_authentication(self, request):
        """
        drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
        如果认证不通过,则会抛异常返回401状态码
        问题: 抛异常会导致视图无法执行
        解决: 捕获异常即可
        """
        try:
            super().perform_authentication(request)
        except Exception as e:
            print('perform_authentication: ', e)

    def get(self, request):
        user = request.user

        redis_conn = get_redis_connection('cart')
        # p1 = redis_conn.pipeline()
        count_list = redis_conn.hvals('cart_%s' % user.id)
        total_count = 0
        for count in count_list:
            count = int(count)
            total_count += count
        data = {
            "total_count": total_count
        }
        return Response(data)


class CartSelectedAllView(APIView):
    def perform_authentication(self, request):
        """
        drf框架在视图执行前会调用此方法进行身份认证(jwt认证)
        如果认证不通过,则会抛异常返回401状态码
        问题: 抛异常会导致视图无法执行
        解决: 捕获异常即可
        """
        try:
            super().perform_authentication(request)
        except Exception as e:
            print('perform_authentication: ', e)

    def put(self, request):

        user = request.user
        if user.is_authenticated():
            serializer = CartSelectedAllSerislizer(data=request.data)
            serializer.is_valid(raise_exception=True)
            selected = serializer.validated_data.get('selected')
            redis_conn = get_redis_connection('cart')
            cart = redis_conn.hgetall('cart_%s' % user.id)
            sku_id_list = cart.keys()
            if selected:  # 全选
                redis_conn.sadd('cart_selected_%s' % user.id, *sku_id_list)
            else:  # 取消全选
                redis_conn.srem('cart_selected_%s' % user.id, *sku_id_list)
            return Response({'message': 'OK'})
