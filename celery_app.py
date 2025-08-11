from celery import Celery
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Celery(
    'automation',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app.conf.beat_schedule = {
    'run-automation-every-2-minutes': {
        'task': 'automation.tasks.run_automation',
        'schedule': 30.0,  # every 2 minutes
    },
}
app.conf.timezone = 'UTC'

# Make sure Celery finds tasks in the automation package
app.autodiscover_tasks(['automation'])
