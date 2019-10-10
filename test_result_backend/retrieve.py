from sqlalchemy import create_engine
import pickle
engine = create_engine(f'mysql://root:ignorance@localhost:3306/')

conn = engine.connect()


def get_task_by_id(task_id):
    sql = f"select * from celery_toys.celery_taskmeta where task_id='{task_id}'"
    proxy = conn.execute(sql)
    res = proxy.fetchall()
    for each in res:
        each = dict(each)
        args = each['args'].decode('u8')
        task_name = each['name']
        result = each['result']
        result = pickle.loads(result)
        print(task_name)
        print(result)


if __name__ == '__main__':
    get_task_by_id('64bd0d35-4b58-4279-837f-35ba51a30161')

