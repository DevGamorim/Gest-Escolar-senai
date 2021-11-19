from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.

#Models banco
from table.models import user

# Bibliotecas externas

import json

@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

def criar_user(request):
    '''
        password
        id_superuser
        username
        first_name
        last_name
        email
        is_staff
        is_active
        privilegio

    '''
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        senha_cripto = make_password(password=tudo['password'], salt=None, hasher='pbkdf2_sha256')
        if tudo['privilegio'] == "adm":
            create = user.objects.create(password=senha_cripto,
            username = tudo['username'],
            first_name = tudo['first_name'],
            last_name = tudo['last_name'],
            email = tudo['email'],
            is_staff =1,
            is_active =1,
            privilegio =tudo['privilegio']
            )
        else:
            create = user.objects.create(password=senha_cripto,
            username = tudo['username'],
            first_name = tudo['first_name'],
            last_name = tudo['last_name'],
            email = tudo['email'],
            is_staff =0,
            is_active =1,
            privilegio =tudo['privilegio']
            )
        print("ok")
    else:
        print("nbbbbb")
    return render(request,'perfil/criar_perfil.html')