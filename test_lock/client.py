# coding=u8
from tasks import shit_task

for i in range(10):
    shit_task.delay('male', i)
    #shit_task.delay('female', i)
