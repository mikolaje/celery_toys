#coding=u8
from celery import Celery
import time



app = Celery('test_cluster', broker='redis://:fixesredis@10.170.0.2:6379/10')

@app.task
def add(x, y):
    time.sleep(30)
    return x + y


