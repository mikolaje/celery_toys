## Start the celery worker as below:
celery -A tasks worker -l info -c 8

测试方式参考test_lock的方式

### 背景
在测试lock task的时候刚开始用pickle 作为序列化方式，但是pickle每次获取的都其实是第一个task，用json的序列化方式则没有这个问题
我猜是pickle 没有把信息序列化完全。
