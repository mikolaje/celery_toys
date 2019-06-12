In this senario, I wanna run only one task at a time, running a new task after one task finished.
It is like the case that there are many people lining up to use the public toilet.

## Start the celery worker as below:
```
celery -A tasks worker -l info -c 8
```
## Start the test client as below:
```
ipython -i client.py
```

