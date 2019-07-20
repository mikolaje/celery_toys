## 启动方式

### 一个服务器上
celery -A tasks -Q q1 worker -l info 

### 另一个服务器上
celery -A tasks -Q q2 worker -l info 
