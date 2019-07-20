from tasks import add, add_in_priority
import time

add.apply_async((1, 1), queue='q1')
add.apply_async((1, 1), queue='q2')


add.apply_async((1, 1), priority=10, queue='q1')
time.sleep(1)
add_in_priority.apply_async((1, 1), priority=0, queue='q1')

