from django.db import models
from django.utils import timezone


class Verified_data(models.Model):
    name = models.CharField(null=True, max_length= 255, verbose_name="Organization Name")
    poc = models.CharField(null=True, max_length=255, verbose_name="Point of Contact")
    phone = models.CharField(null=True, max_length=255, verbose_name="Phone")
    address = models.CharField(null=True, max_length=255, verbose_name="Address", )
    pincode = models.CharField(null=True, max_length=20, verbose_name="Pincode")
    notes = models.TextField(null=True, verbose_name="Notes")
    email = models.CharField(null=True, max_length=255, verbose_name="Email")
    verified_status = models.CharField(max_length=20 ,default='N', verbose_name="Status")
    verified_date = models.DateTimeField(default=timezone.now, null=True, verbose_name="Verfied Date")
    verified_by = models.CharField(null=True, max_length=255, verbose_name="Verified By")
    city = models.CharField(max_length=100, verbose_name="City")
    category = models.CharField(max_length=100, verbose_name="Category")

    class Meta:
        db_table = "isb_data"
