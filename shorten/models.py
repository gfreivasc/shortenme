from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
import string

# Create your models here.
class Link(models.Model):
    real_url = models.TextField(default='https://google.com')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.real_url
    
    def get_absolute_url(self):
        return reverse('link-details', kwargs={'pk': self.pk})
        
    def get_hash(self):
        hash_alphabet = string.ascii_lowercase
        hash_alphabet += string.ascii_uppercase
        hash_alphabet += ''.join(str(x) for x in xrange(9))
        
        fpk = self.pk + 238328 # base de 3 letras do alfabeto
        
        digitos = []
        
        while fpk > 0:
            digitos.append(fpk % 62)
            fpk /= 62
            
        digitos.reverse()
        return ''.join(hash_alphabet[i] for i in digitos)