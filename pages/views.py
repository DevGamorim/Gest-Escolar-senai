from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.

#Models banco
from table.models import user, endereco, pessoa

# Bibliotecas externas

import json

@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

def criar_user(request):
    if request.method == 'POST':
        # salva todas informações do usuario em um array
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)

        #criptografa a senha do novo usuario
        senha_cripto = make_password(password=tudo['password'], salt=None, hasher='pbkdf2_sha256')

        #criptografa a senha do novo usuario
        if tudo['privilegio'] == "adm":
            usuario = user.objects.create(password=senha_cripto,
            username = tudo['username'],
            first_name = tudo['first_name'],
            last_name = tudo['last_name'],
            email = tudo['email'],
            is_staff =1,
            is_active =1,
            privilegio =tudo['privilegio']
            )
        else:
            usuario = user.objects.create(password=senha_cripto,
            username = tudo['username'],
            first_name = tudo['first_name'],
            last_name = tudo['last_name'],
            email = tudo['email'],
            is_staff =0,
            is_active =1,
            privilegio =tudo['privilegio']
            )
        
        endereco_ = endereco.objects.create(
            bairro = tudo['bairro'],
            rua = tudo['rua'],
            numero = tudo['numero'],
            complemento = tudo['complemento']
        )

        pessoa_ = pessoa.objects.create(
            nome = str(tudo['first_name'])+" "+str(tudo['last_name']),
            cpf = tudo['cpf'],
            nascimento = tudo['nascimento'],
            endereco = endereco_,
            usuario = usuario
        )
        print("create")
    else:
        print("nbbbbb")
    return render(request,'perfil/criar_perfil.html')
