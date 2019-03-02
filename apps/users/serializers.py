import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.settings import api_settings

from users.models import User, Address


class CreateUserSerializer(serializers.ModelSerializer):
    """注册用户接口使用的序列化器
    """
    password2 = serializers.CharField(label='确认密码', min_length=8, max_length=20, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, write_only=True)
    allow = serializers.BooleanField(label='同意用户协议', default=False, write_only=True)
    token = serializers.CharField(label='登录状态', read_only=True)
    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value
    def validate_allow(self, value):
        """检验用户是否同意协议"""
        if not value:
            raise serializers.ValidationError('请同意用户协议')
        return value
    def validate(self, attrs):
        # 判断两次密码
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码不一致')
        mobile = attrs.get('mobile')
        # 判断短信验证码
        strict_redis = get_redis_connection('verify_codes')  # type: StrictRedis
        # 获取redis中保存的正确的短信验证码
        real_sms_code = strict_redis.get('sms_%s' % mobile)   # bytes -> str
        if real_sms_code is None:
            raise ValidationError('验证码无效')
        # 获取用户传递的短信验证码
        sms_code = attrs.get('sms_code')
        # 比较短信验证码是否相等, 不相等提示出错信息
        if real_sms_code.decode() != sms_code:
            raise ValidationError('验证码不正确')
        return attrs
    def create(self, validated_data):
        # 自定义保存一条用户数据, 指定要保存哪些字段
        # user = User.objects.create(                   # 密码不会加密
        user = User.objects.create_user(                # 会对密码加密
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            mobile=validated_data.get('mobile')
        )

        # 注册成功自动登陆　需生成ｊｗｔ并返回给客户端

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # {'user_id': 12, 'email': '', 'username': '13600000000', 'exp': 1539048426}
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token  # 生成的jwt 序列化返回
        return user
    class Meta:
        model = User   # 关联的模型类
        fields = ('id', 'username', 'password', 'mobile',
                  'password2', 'sms_code', 'allow', 'token')
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

class UserAddressSerializer(ModelSerializer):

    """地址管理的序列化器"""

    # 需求: 序列时,返回省市区的名称, 而不是默认返回主键id
    province = StringRelatedField(read_only=True)
    city = StringRelatedField(read_only=True)
    district = StringRelatedField(read_only=True)

    # 新增三个属性: 新地址时用到
    province_id = serializers.IntegerField(label='省ID')
    city_id = serializers.IntegerField(label='市ID')
    district_id = serializers.IntegerField(label='区ID')

    def create(self, validated_data):
        # 在新增一条地址数据时, 需要自动设置user字段, 因为用户没有传递此字段给服务器
        validated_data['user'] = self.context.get('request').user

        return super().create(validated_data)  # 新增一条地址数据
        # Address.objects.create(receiver=xx, title=xx, province_id=xx, city_id=xx..)

    class Meta:
        model = Address
        # fields = ('id',)
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')