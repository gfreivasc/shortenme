from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from .models import Link
import string
import requests

class IndexView(TemplateView):
    template_name = "shorten/index.html"
    def get(self, request):
        r = requests.get('http://httpbin.org/status/418')
        return render(request, 'shorten/index.html', {'text': r.text})

class LinkRedirectView(View):
    def __init__(self):
        self.hash_alphabet = string.ascii_lowercase
        self.hash_alphabet += string.ascii_uppercase
        self.hash_alphabet += ''.join(str(x) for x in xrange(9))
    
    # Transformar hash do link pra pk da db
    def _hash_to_pk(self, hash):
        digitos = list(hash)
        
        pk = 0
        i = len(digitos)
        for a in digitos:
            pk += self.hash_alphabet.index(a)**i
            i -= 1
        
        return pk - 1
        
    def get(self, request, hash):
        link = Link.objects.get(pk=self._hash_to_pk(hash))
        return HttpResponseRedirect(link.real_url)

class LinkDetails(TemplateView):
    template_name = "shorten/link_details.html"
    
    def __init__(self):
        self.hash_alphabet = string.ascii_lowercase
        self.hash_alphabet += string.ascii_uppercase
        self.hash_alphabet += ''.join(str(x) for x in xrange(9))
        
    def _pk_to_hash(self, pk):
        pk += 238328 # base de 3 letras do alfabeto
        
        digitos = []
        
        while pk > 0:
            digitos.append(pk % 62)
            pk /= 62
            
        digitos.reverse()
        return ''.join(self.hash_alphabet[i] for i in digitos)
        
    def get(self, request, pk):
        url = 'https://shortenme.herokuapp.com/'
        url += self._pk_to_hash(int(pk))
        return render(request, 'shorten/link_details.html', {'url': url})
    
class LinkCreate(CreateView):
    model = Link
    fields = ['real_url']