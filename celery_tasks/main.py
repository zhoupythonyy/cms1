from celery import Celery
import os
# 设置配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'cms.settings')

# 创建一个celery应用
celery_app = Celery('cms', broker='redis://127.0.0.1:6379/15')

# 指定扫描任务的包,会自动读取包下的名字为 tasks.py 的文件
celery_app.autodiscover_tasks(['celery_tasks.sms'])


# 启动celery
# celery -A celery_tasks.main worker -l info
