from django.db import models
from jsonfield import JSONField


class UserData(models.Model):
    uid = models.BigIntegerField()
    passwords = JSONField()