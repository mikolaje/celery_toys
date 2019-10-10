#coding=u8
from celery import Celery
import time


result_backend = 'db+mysql://root:ignorance@localhost/celery_toys'

app = Celery('test_result_backend')

app.conf.update(
    broker_url='redis://localhost:6379/10',
    result_backend=result_backend,
    result_extended=True
)


@app.task(bind=True, name='add')
def add(self, x, y):
    self.request.task_name = 'add'
    time.sleep(5)
    return x + y


@app.task(bind=True, name='add_in_priority')
def add_in_priority(self, x, y, z=None, v='测试'):
    self.request.task_name = 'add_in_priority'
    time.sleep(5)
    return x + y

