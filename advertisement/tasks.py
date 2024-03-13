from ehyzmat.celery import app
from services.models import Service
from advertisement.models import Advertisement
from datetime import date


@app.task
def advertisement_vip_task():
    checking_services = Service.objects.filter(vip_date=date.today(), vip_is_active=True)
    checking_advertisements = Advertisement.objects.filter(expired_date=date.today(), is_active=True)
    print("Checking services' V.I.P expired times...")
    for i in checking_services:
        i.vip_is_active = False
        i.vip_date = None
        i.save()
    print("Process done.")
    print("Checking advertisements' expired times...")
    for i in checking_advertisements:
        i.is_active = False
        i.expired_date = None
        i.save()
    print("Process done.")