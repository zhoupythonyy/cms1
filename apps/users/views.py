from gc import get_objects

from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from users import serializers
from users.models import User
from users.serializers import UserAddressSerializer


def test(request):
    return HttpResponse("项目测试11")


class UsernameCountView(APIView):
    """
    用于获取用户名并判断是否已存在的视图
    # GET    /usernames/(?P<username>\w{5, 20})/count/
    """
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        data = {
            "username": username,
            "count": count,
        }

        return Response(data)


class CreateUserView(CreateAPIView):
    """
    注册用户  POST   /register/
    """
    serializer_class = serializers.CreateUserSerializer


class MyObtainJSONWebToken(ObtainJSONWebToken):
    """
    自定义登陆接口　重写post 请求时传递用户名密码　判断是否正确　
    返回　id name token
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        s = self.get_serializer(data=request.data)

        if s.is_valid():
            user = s.validated_data.get("user")
            # 合并购物车
            # merge_cart_cookie_to_redis(request, response, user)
        return response


class AddressViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    """ 用户地址管理: 6个接口
    1. 地址增删改查（查多条）  4个
    2. 设置默认地址: put
    3. 设置地址标题: put
    """
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]  # 登录才能调用

    # queryset = Address.objects.all()
    def get_queryset(self):
        # 返回当前登录用户所有的地址
        return self.request.user.addresses.filter(is_deleted=False)

    # def post(self, request):
    #     return create()

    # 需求: 限制返回的地址个数
    def create(self, request, *args, **kwargs):
        count = request.user.addresses.count()
        if count >= 5:  # 每个用户最多不能超过2个地址
            return Response({'message': '地址个数已达到上限'}, status=400)

        return super().create(request, *args, **kwargs)

    # 重写list方法
    def list(self, request, *args, **kwargs):
        """ 用户地址列表数据 """
        queryset = self.get_queryset()  # 当前登录用户的所有地址
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'user_id': request.user.id,
            'default_address_id': request.user.default_address_id,
            'limit': 10,
            'addresses': serializer.data  # 列表
        })

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.user.default_address_id = obj.id

        return super().update(request, *args, **kwargs)


