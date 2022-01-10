import os

"""
Celeryの設定ファイル
- djangoと共有する設定または開発/本番で異なる設定は.env.***に書くこと
- それ以外は直接ここに書く
"""

broker_url = os.environ.get('CELERY_BROKER_URL')
timezone = os.environ.get('TIMEZONE')
worker_concurrency = os.environ.get('CELERY_WORKER_CONCURRENCY')
