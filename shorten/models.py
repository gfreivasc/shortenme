from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
class Link(models.Model):
    real_url = models.TextField(default='https://google.com')
    
    def get_absolute_url(self):
        return reverse('link-details', kwargs={'pk': self.pk})