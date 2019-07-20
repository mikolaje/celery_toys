## 启动方式

### 一个服务器上
celery -A tasks -Q q1 worker -l info 

### 另一个服务器上
celery -A tasks -Q q2 worker -l info 

# 测试集群多个worker
## Test Result
如果用同一个queue，则每个worker消费同一个queue，哪个worker先闲着就先执行任务

通过不同的Queue来启动不同worker，可以在task中指定要哪个worker来执行任务

# 测试任务的优先顺序

## Test Result
although you trigger the add task first, there is a priority for add_in_priority task. 
As a result, you can see the add_in_priority task come out prior than add task.
