#coding=u8
from celery import Celery
import time



app = Celery('test_cluster', broker='redis://:fixesredis@10.170.0.2:6379/10')

@app.task(bind=True)
def add(self, x, y):
    time.sleep(30)
    return x + y


@app.task(bind=True)
def add_in_priority(self, x, y):
    time.sleep(30)
    return x + y
