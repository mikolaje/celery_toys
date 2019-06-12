#coding=u8
from celery import Celery
import time
import requests
import asyncio
from threading import Thread


app = Celery('tasks', broker='redis://localhost:6379/10')


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


@app.task
def add(x, y):
    time.sleep(30)
    return x + y

def req():
    res = requests.get('http://baidu.com')
    print(res)
    return 'hehe'


async def req_async():
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    #coro1 = loop.run_in_executor(None, req)
    #coro2 = loop.run_in_executor(None, req)
    #res = await asyncio.gather(coro1, coro2)
    res = await asyncio.sleep(3)
    return 'test'

def m_threads():
    res = requests.get('http://baidu.com')
    return res

@app.task
def async_test():
    """会有奇怪的报错：ValueError: loop argument must agree with Future  ensure_future 命名没有调用错的"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    task = asyncio.ensure_future(asyncio.sleep(3))

    loop.run_until_complete(task)

    res = task.result()
    print(res)

@app.task
def thread_test():
    t = ThreadWithReturnValue(target=m_threads, args=())
    t.start()
    res = t.join()
    print(res)
    #print(t.is_alive())

