from ehyzmat.celery import app
from services.models import Service
from datetime import date


@app.task
def service_vip_task():
    checking_services = Service.objects.filter(vip_date=date.today(), vip_is_active=True)
    for i in checking_services:
        i.vip_is_active = False
        i.vip_date = None
        i.save()