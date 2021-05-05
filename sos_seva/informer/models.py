from django.db import models

# Create your models here.
class tweet(models.Model):
    text = models.TextField(null = True)
    place = models.TextField(null=True)
    date = models.DateTimeField(null=True)
    label = models.TextField(null = True)
    keyword = models.CharField(null = True, max_length=100)
    class Meta:
        db_table = "tweet_data"

