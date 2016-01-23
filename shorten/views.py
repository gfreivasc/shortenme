from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from .models import Link
from .forms import UserCreationForm, LinkForm
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
        
    def get(self, request, pk):
        url = 'https://shortenme.herokuapp.com/'
        url += Link.objects.get(pk=pk).get_hash()
        return render(request, 'shorten/link_details.html', {'url': url})
    
class LinkCreate(CreateView):
    model = Link
    form_class = LinkForm
    
    def form_valid(self, form):
        valid = super(LinkCreate, self).form_valid(form)
        if (valid):
            link = form.save(commit=False)
            link.owner = self.request.user
            link = link.save()
        return valid

"""    
def db(request):

    link = Link()
    link.save()

    links = Link.objects.all()

    return render(request, 'shorten/db.html', {'links': links})
"""

class UserCreate(CreateView):
    form_class = UserCreationForm
    template_name = 'shorten/registration.html'
    success_url = '/'
    
    def form_valid(self, form):
        valid = super(UserCreate, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        new_user = authenticate(username=username, password=password)
        # login(self.request, new_user)
        return valid
        
class UserLinks(TemplateView):
    def get(self, request):
        links = Link.objects.filter(owner=request.user)
        return render(request, 'shorten/links_list.html', {'links': links})