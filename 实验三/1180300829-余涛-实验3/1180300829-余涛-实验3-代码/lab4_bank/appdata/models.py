from django.db import models


class bankuser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    passwd = models.CharField(max_length=50)
    currency = models.IntegerField()
    isadmin = models.BooleanField()

