from ehyzmat.celery import app
from django.core.management import call_command


@app.task
def flushexpiredtokens_t():
    call_command('flushexpiredtokens')