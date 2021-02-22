from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time


'''
@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    result = 0
    for i in range(seconds):
        time.sleep(1)
        result += i
        progress_recorder.set_progress(i + 1, seconds)
    return result
'''

@shared_task
def do_something():
    bar = ProgressBar(
        task_id=do_something.request.id,
        total=10,
        step='Drying kelp...'
    )

    # some_work()
    bar.update(
        progress='5',
        step='Making sushi...'
    )

    # some_more_work()
    bar.progress.finalize()