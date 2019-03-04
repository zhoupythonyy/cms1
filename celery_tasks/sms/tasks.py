from celery_tasks.main import celery_app
from libs.yuntongxun.sms import CCP


@celery_app.task(name='sms_code')
def send_sms_code(mobile, sms_code):
    # CCP().send_template_sms(mobile, [sms_code, 5], 1)
    print('发送短信验证码:', sms_code)

