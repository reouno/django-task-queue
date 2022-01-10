import time

from celery import Celery

app = Celery('api_server')

app.config_from_object('api_server.celeryconfig')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self, arg=None):
    print(f'Arg: {arg}, Request: {self.request!r}')


@app.task(bind=True)
def sleep_task(self, sec=1, arg=None):
    time.sleep(sec)
    print(f'{sec} have passed. Arg: {arg}, Request: {self.request!r}')
