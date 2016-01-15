from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Link(models.Model):
    real_url = models.TextField(default='https://google.com')