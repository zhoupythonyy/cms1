import random

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.yuntongxun.sms import CCP


class SMSCodeView(APIView):
    """
    获取短信验证码的视图函数

    GET    /sms_code/(?P<mobile>1[3-9]\d{9})/

    实现：
    1. 创建链接redis数据库的对象
    2. 校验短信验证码是否重复发送 设置60秒内禁止重复发送
    3. 生成和发送短信验证码
    4. 保存短信验证码
    5. 响应短信验证码
    """
    def get(self, request, mobile):
        # 1. 创建链接redis数据库的对象
        redis_conn = get_redis_connection('verify_codes') # type: StrictRedis

        # 2. 校验短信验证码是否重复发送 设置60秒内禁止重复发送
        # 3. 生成和发送短信验证码  调用云通讯接口
        sms_code = "%06d" % random.randint(0, 999999)
        print(sms_code)

        # CCP().send_template_sms(mobile, [sms_code, 5], 1)

        # 4. 保存短信验证码redis数据库 -- setex 表示设置有效期的键值
        redis_conn.setex("sms_%s" % mobile, 5*60, sms_code)
        # redis_conn.setex("send_flag_%s" % mobile, 60, 1)

        # 5. 响应短信验证码
        return Response({"message": "ok"})
