# coding=u8
from celery import Celery, Task
from celery.exceptions import Ignore
from celery.states import SUCCESS, PENDING, STARTED
from celery import task
import redis
import json
import pickle
import logging
from celery.five import monotonic
from celery.utils.log import get_task_logger
from contextlib import contextmanager
from django.core.cache import cache
from hashlib import md5
import time

app = Celery('tasks', broker='redis://localhost:6379/10')

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes

rdb = redis.Redis(db=11, charset="utf-8")

class ShitTask(Task):
    abstract = True

    #def on_failure(self, exc, task_id, args, kwargs, einfo):
        #logging.info('Task failed')

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if retval == 'I finished shit':
            print('somebody finished shit, calling the next one to shit')
            shit_queue = '{0}-queue'.format(self.name)
            print('shit queue %s' % shit_queue)
            weird_pending_task = rdb.rpop(shit_queue)

            if weird_pending_task:
                weird_task = pickle.loads(weird_pending_task)
                print('pending task %s' % (weird_task.request))  # the task is always the first task acquired the lock, don't know why
                weird_task.delay(*args)
        else:
            pass


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = monotonic() + LOCK_EXPIRE - 3

    status = rdb.setnx(lock_id, oid)
    rdb.expire(lock_id, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if monotonic() < timeout_at and status:
            # you can not engage the toilet for too long, there is a time limit.
            print('release the lock and open the door of the toilet %s' % lock_id)
            rdb.delete(lock_id)


@app.task(bind=True, base=ShitTask, max_retries=1)
def shit_task(self, gender):
    print('task name %s' % self.name)
    lock_id = '{0}-lock'.format(self.name)
    shit_queue = '{0}-queue'.format(self.name)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        print('acquired: %s' % acquired)
        if acquired:
            print('Oh yes, Lock the door and it is my time to shit. [in %s toilet]' % gender)
            time.sleep(10)
            return 'I finished shit'
        else:
            print('Oops, somebody engaged the toilet, I have to queue up')
            pending_task = pickle.dumps(self)
            print('dump task %s' % self.request)
            rdb.lpush(shit_queue, pending_task)
            #pending_task2 = rdb.rpop(shit_queue)
            #task2 = pickle.loads(pending_task2)  # 这里rpop 然后 loads出来的是正常的
            #print('test task %s' % task2.request)  # here the task pickle loaded is normal
            raise Ignore()
