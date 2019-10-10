## 需求背景
想通过Flower中查看失败的task，然后手动重新执行失败的task. 我在Flower的PR上看到13年就有类似的需求。
不过却一直没有merged到主分支上 https://github.com/mher/flower/pull/158

所以那就只能自己改代码了。

在此我想测试下能否将task的一些元数据保存在RDB上。比如保存在MySQL里。

## 启动worker
watchmedo auto-restart -- celery worker -l info -A tasks

## 实验结果
在加了result_backend参数之后，在MySQL中会多 `celery_taskmeta` and `celery_tasksetmeta` 两个表。

### Celery 4.4 new feature
```
app.conf.update(
    broker_url='redis://localhost:6379/10',
    result_backend=result_backend,
    result_extended=True
)
```
在Celery 4.4 后可以加上result_extended参数，会把args和kwargs也保存在表里面。

