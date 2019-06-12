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
            task_args = rdb.rpop(shit_queue)
            if task_args:
                task_args = json.loads(task_args)
                self.delay(*task_args)
        else:
            pass


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = monotonic() + LOCK_EXPIRE - 3
    # status = cache.add(lock_id, oid, LOCK_EXPIRE)  # 如果lock_id 存在则返回False，如果不存在则返回True
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
def shit_task(self, gender, number):
    print('task name %s' % self.name)
    lock_id = '{0}-lock'.format(self.name)
    shit_queue = '{0}-queue'.format(self.name)
    with memcache_lock(lock_id, self.app.oid) as acquired:
        print('acquired: %s' % acquired)
        if acquired:
            print('Oh~, Lock the door and it is my time to shit. [in %s toilet], My number is [%s]' % (gender, number))
            time.sleep(10)
            return 'I finished shit'
        else:
            print('Oops, somebody engaged the toilet, I have to queue up')
            rdb.lpush(shit_queue, json.dumps(list(self.request.args)))
            raise Ignore()
