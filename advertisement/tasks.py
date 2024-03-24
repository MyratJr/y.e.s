from ehyzmat.celery import app
from advertisement.models import Advertisement, AdvertisementChoises
from datetime import date


@app.task
def advertisement_vip_task():
    checking_advertisements = Advertisement.objects.filter(expired_date=date.today(), status=AdvertisementChoises.Kabul_Edildi)
    for i in checking_advertisements:
        i.status = AdvertisementChoises.Mohleti_Gutardy
        i.expired_date = None
        i.save()