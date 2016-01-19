from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
import string
import requests

class IndexView(TemplateView):
    template_name = "index.html"
    def get(self, request):
        r = requests.get('http://httpbin.org/status/418')
        return render(request, 'index.html', {'text': r.text})

# Create your views here.
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
        
        return pk
        
    def get(self, request, hash):
        link = Link.objects.get(pk=_hash_to_pk(hash))
        return HttpResponseRedirect(link.real_url)
        
class LinksView(View):
    def __init__(self):
        self.hash_alphabet = string.ascii_lowercase
        self.hash_alphabet += string.ascii_uppercase
        self.hash_alphabet += ''.join(str(x) for x in xrange(9))

    # Transformar PK da entrada no db em hash pra link
    def _pk_to_hash(self, pk):
        pk += 238328 # base de 3 letras do alfabeto
        
        digitos = []
        
        while pk > 0:
            digitos.append(pk % 62)
            pk /= 62
            
        digitos.reverse()
        return ''.join(self.hash_alphabet[i] for i in digitos)
        
    def post(self, request):
        link = Link()
        link = request.POST.get('link', '')
        link.save
        
        return HttpResponse(status=201)