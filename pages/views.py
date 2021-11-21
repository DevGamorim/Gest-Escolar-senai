from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.

# Models banco
from table.models import user, endereco, pessoa, professor, disciplina, aluno, nota, turma
from table.models import turma_tem_disciplina, turma_tem_aluno, curso, turma_tem_curso

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
        print(tudo['privilegio'])
        # criptografa a senha do novo usuario
        senha_cripto = make_password(
            password=tudo['password'], salt=None, hasher='pbkdf2_sha256')

        # criptografa a senha do novo usuario
        if tudo['privilegio'] == "adm":
            usuario = user.objects.create(password=senha_cripto,
                                          username=tudo['username'],
                                          first_name=tudo['first_name'],
                                          last_name=tudo['last_name'],
                                          email=tudo['email'],
                                          is_staff=1,
                                          is_active=1,
                                          privilegio=tudo['privilegio']
                                          )
        else:
            usuario = user.objects.create(password=senha_cripto,
                                          username=tudo['username'],
                                          first_name=tudo['first_name'],
                                          last_name=tudo['last_name'],
                                          email=tudo['email'],
                                          is_staff=0,
                                          is_active=1,
                                          privilegio=tudo['privilegio']
                                          )

        endereco_ = endereco.objects.create(
            bairro=tudo['bairro'],
            rua=tudo['rua'],
            numero=tudo['numero'],
            complemento=tudo['complemento']
        )

        pessoa_ = pessoa.objects.create(
            nome=str(tudo['first_name'])+" "+str(tudo['last_name']),
            cpf=tudo['cpf'],
            nascimento=tudo['nascimento'],
            endereco=endereco_,
            usuario=usuario
        )
        if tudo['privilegio'] == "prof":
            novo = professor.objects.create(pessoa=pessoa_,
                                            matricula=tudo['matricula']
                                            )
        elif tudo['privilegio'] == "aluno":
            novo = aluno.objects.create(pessoa=pessoa_,
                                        matricula=tudo['matricula']
                                        )
        print("create")
    else:
        print("nbbbbb")
    return render(request, 'perfil/criar_perfil.html')


def perfil(request):
    user_name = request.user
    usuario = user.objects.get(username=user_name)
    pessoa_ = pessoa.objects.get(usuario=str(usuario.id))

    # criar um local aonde mostra o perfil
    return render(request, 'perfil/criar_perfil.html')


def nova_disciplina(request):
    usuario = user.objects.filter(privilegio="prof")
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)
        prof = professor.objects.get(pessoa=str(tudo['professor']))
        nova_disciplina = disciplina.objects.create(
            nome=tudo['nome'],
            carga_horaria=tudo['carga_horaria'],
            professor=prof
        )
        print(nova_disciplina, "é um nova disciplina")
    return render(request, 'atribuir/nova_disciplina.html', {"professor": usuario})


def lancamento_nota(request):

    # bimestre
    # falta
    # nota
    # aluno
    # disciplina
    usuario = user.objects.filter(privilegio="aluno")
    disc = disciplina.objects.all()
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)

        pessoa_ = pessoa.objects.get(usuario=tudo['aluno'])
        print(pessoa_.nome, pessoa_.id)
        aluno_ = aluno.objects.get(pessoa=pessoa_)
        disciplina_ = disciplina.objects.get(pk=tudo['disciplina'])
        print(disciplina_.nome)
        lanca_nota = nota.objects.create(
            bimestre=tudo['bimestre'],
            falta=tudo['falta'],
            nota=tudo['nota'],
            aluno=aluno_,
            disciplina=disciplina_
        )

    return render(request, 'atribuir/nova_nota.html', {"alunos": usuario, "disciplinas": disc})


def criar_turma(request):
    # nome
    # semestre
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)
        new_turma = turma.objects.create(
            nome=tudo['nome'],
            semestre=tudo['semestre']
        )
    return render(request, 'atribuir/nova_turma.html', {})


def adicionar_diciplica_a_turma(request):
    disc = disciplina.objects.all()
    turmas = turma.objects.all()
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)
        disciplina_ = disciplina.objects.get(pk=tudo['disciplina'])
        turma_ = turma.objects.get(pk=tudo['turma'])
        create_turma_tem_disciplina = turma_tem_disciplina.objects.create(
            disciplina=disciplina_,
            turma=turma_
        )
    return render(request, 'atribuir/adicionar_diciplica_a_turma.html', {"disciplinas": disc, "turmas": turmas})


def adicionar_turma_tem_aluno(request):
    turmas = turma.objects.all()
    alunos = aluno.objects.all()
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)

        aluno_ = aluno.objects.get(pk=str(tudo['aluno']))
        turma_ = turma.objects.get(pk=str(tudo['turma']))

        criar_turma_aluno = turma_tem_aluno.objects.create(
            aluno=aluno_,
            turma=turma_
        )
        print(criar_turma_aluno)
    return render(request, 'atribuir/adicionar_turma_tem_aluno.html', {"turmas": turmas, "alunos": alunos})


def criar_curso(request):
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)

        novo_curso = curso.objects.create(
            nome=tudo['nome'],
            tipo=tudo['tipo']
        )

    return render(request, 'atribuir/criar_curso.html', )


def criar_turma_tem_curso(request):
    turmas = turma.objects.all()
    cursos = curso.objects.all()
    #turma = models.ForeignKey(turma, on_delete=models.CASCADE)
    #curso = models.ForeignKey(curso, on_delete=models.CASCADE)

    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)

        turma_ = turma.objects.get(pk=tudo['turma'])
        curso_ = curso.objects.get(pk=tudo['curso'])

        nova_turma_tem_curso = turma_tem_curso.objects.create(
            turma=turma_,
            curso=curso_
        )
    return render(request, 'atribuir/criar_turma_tem_curso.html', {'turmas': turmas, 'cursos': cursos})
