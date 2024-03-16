from ehyzmat.celery import app
from advertisement.models import Advertisement
from datetime import date


@app.task
def advertisement_vip_task():
    checking_advertisements = Advertisement.objects.filter(expired_date=date.today(), is_active=True)
    for i in checking_advertisements:
        i.is_active = False
        i.expired_date = None
        i.save()