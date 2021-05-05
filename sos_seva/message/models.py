from django.db import models
import django
import datetime
from django.utils import timezone
# Create your models here.
class WhatsAppUsers(models.Model):
    STATUS_TYPES = (
        ('Submitted', 'Submitted'),
        ('Opened', 'Opened'),
        ('Responded', 'Responded'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
        ('Released', 'Released')
    )
    # id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=256)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=256)
    pincode = models.IntegerField()
    purpose = models.TextField()
    other_details = models.TextField(null=True)
    rank = models.CharField(max_length=128, default='', blank=True, null=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    assigned_to = models.CharField(max_length=128, default='-', null=True)
    ticket_status = models.CharField(
        max_length=200, choices=STATUS_TYPES, default='Submitted',
        help_text='<b>Submitted:</b> This is when an employee has utilized SOS seva and raised a query<br/><b>Opened:</b> A volunteer puts it in a state to work on it. No other volunteer can see this ticket post this.<br/><b>Responded:</b> A volunteer has reached out to the employee by a WhatsAppUsers message<br/><b>Resolved:</b> Ticket resolved from a volunteer/Information provided<br/><b>Closed:</b> Employee query resolved and employee is satisfied<br/><b>Released:</b> A volunteer cannot solve this. Releasing it back in the pool')
    opened_time = models.DateTimeField(default=django.utils.timezone.now)
    responded_time = models.DateTimeField(default=django.utils.timezone.now)
    resolved_time = models.DateTimeField(default=django.utils.timezone.now)
    closed_time = models.DateTimeField(default=django.utils.timezone.now)
    released_time = models.DateTimeField(default=django.utils.timezone.now)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s" % (self.username)

    class Meta:
       # managed = False
       db_table = 'whatsapp_users'


class CoordinatingBodies(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=256)
    pincode = models.IntegerField()
    status = models.BooleanField(default=True)
    created = models.DateTimeField(default=django.utils.timezone.now, editable=False)

    class Meta:
       # managed = False
       db_table = 'coordinating_bodies'


class RankMaster(models.Model):
    # id = models.IntegerField(primary_key=True)
    rank_name = models.CharField(max_length=256)
    keywords = models.TextField()

    class Meta:
        # managed = False
        db_table = 'rank_master'