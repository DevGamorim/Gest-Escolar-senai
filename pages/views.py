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
from datetime import datetime
import statistics
import math
from scipy import stats
import numpy
from collections import Counter


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
    return render(request, 'adm/criar_perfil.html')


def perfil(request):
    user_name = request.user
    usuario = user.objects.get(username=user_name)
    pessoa_ = pessoa.objects.get(usuario=str(usuario.id))

    # criar um local aonde mostra o perfil
    return render(request, 'perfil/ver_perfil.html', {"pessoa": pessoa_})


def nova_disciplina(request):
    usuario = user.objects.filter(privilegio="prof")
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)
        pessoa_ = pessoa.objects.get(usuario=str(tudo['professor']))
        prof = professor.objects.get(pessoa=str(pessoa_.id))
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
    # turma = models.ForeignKey(turma, on_delete=models.CASCADE)
    # curso = models.ForeignKey(curso, on_delete=models.CASCADE)

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


def minhas_turmas(request):
    lista = []
    user_name = request.user
    usuario = user.objects.get(username=user_name)
    pessoa_ = pessoa.objects.get(usuario=str(usuario.id))
    professor_ = professor.objects.get(pessoa=str(pessoa_.id))
    disciplinas = disciplina.objects.filter(professor=str(professor_.id))
    for n in range(0, len(disciplinas)):
        turmas = turma_tem_disciplina.objects.filter(
            disciplina=str(disciplinas[n].id))
        for m in range(0, len(turmas)):
            print(turmas[m])
            lista.append(turmas[m])
    return render(request, 'menu/turma.html', {'disciplinas': lista})


def agendar_aula(request, id):
    horarios = []
    turma_ = turma_tem_disciplina.objects.get(pk=str(id))
    horario_ = turma_tem_disciplina.objects.filter(status_agendamento=True)
    for n in range(0, len(horario_)):
        dia = horario_[n].data_e_hora
        dia = dia.strftime("%Y/%m/%d")
        print(dia)
        horarios.append(dia)
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)
        turma_ = turma_tem_disciplina.objects.get(pk=str(tudo['disciplina']))
        data = str(tudo['date'])+" 17:10:00"
        data = datetime.fromisoformat(data)
        print(data)
        turma_pesquisa = turma_tem_disciplina.objects.filter(data_e_hora=data)
        if len(turma_pesquisa) <= 0:
            turma_.data_e_hora = data
            turma_.save()
            lista = []
            user_name = request.user
            usuario = user.objects.get(username=user_name)
            pessoa_ = pessoa.objects.get(usuario=str(usuario.id))
            professor_ = professor.objects.get(pessoa=str(pessoa_.id))
            disciplinas = disciplina.objects.filter(professor=str(professor_.id))
            for n in range(0, len(disciplinas)):
                turmas = turma_tem_disciplina.objects.filter(
                    disciplina=str(disciplinas[n].id))
                for m in range(0, len(turmas)):
                    print(turmas[m])
                    lista.append(turmas[m])
            return render(request, 'menu/turma.html', {'disciplinas': lista})
        else:
            return render(request, 'menu/agendamento.html', {'turma': turma_, 'horarios': horarios,'alerta':'Data ja indisponivel!'})
    return render(request, 'menu/agendamento.html', {'turma': turma_, 'horarios': horarios,})


def notas_e_faltas(request):
    lista = []
    user_name = request.user
    usuario = user.objects.get(username=user_name)
    pessoa_ = pessoa.objects.get(usuario=str(usuario.id))
    professor_ = professor.objects.get(pessoa=str(pessoa_.id))
    disciplinas = disciplina.objects.filter(professor=str(professor_.id))
    for n in range(0, len(disciplinas)):
        turmas = turma_tem_disciplina.objects.filter(
            disciplina=str(disciplinas[n].id))
        for m in range(0, len(turmas)):
            print(turmas[m])
            lista.append(turmas[m])
    return render(request, 'menu/notas_e_faltas.html', {'disciplinas': lista})


def lista_alunos_notas_e_faltas(request, id, disci):
    alunos = turma_tem_aluno.objects.filter(turma=str(id))
    disciplina_ = disciplina.objects.get(pk=disci)
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)
    return render(request, 'menu/lista_alunos_notas_e_faltas.html', {'alunos': alunos,'disciplina':disci})


def visualizar_notas(request, id, disci):
    aluno_ = aluno.objects.get(pk=id)
    notas = nota.objects.filter(aluno=id , disciplina = disci) 
    if request.method == 'POST':
        tudo = request.POST.copy()
        tudo = json.dumps(tudo)
        tudo = json.loads(tudo)
        print(tudo)
    
        aluno_ = aluno.objects.get(pk=id)
        disciplina_ = disciplina.objects.get(pk=disci)
        
        if len(tudo['1bimestre']) >= 1:
            if len(tudo['1falta']) >= 1:
                notas = nota.objects.create(
                    bimestre=1,
                    falta=tudo['1falta'],
                    nota=tudo['1bimestre'],
                    aluno=aluno_,
                    disciplina=disciplina_
                )
            else:
                return render(request, 'menu/visualizar_nota.html', {'notas': notas,'status':len(notas),'aluno':aluno_})
        else:
            return render(request, 'menu/visualizar_nota.html', {'notas': notas,'status':len(notas),'aluno':aluno_})
        
        if len(tudo['2bimestre']) >= 1:
            if len(tudo['2falta']) >= 1:
                notas = nota.objects.create(
                    bimestre=2,
                    falta=tudo['2falta'],
                    nota=tudo['2bimestre'],
                    aluno=aluno_,
                    disciplina=disciplina_
                )
            else:
                return render(request, 'menu/visualizar_nota.html', {'notas': notas,'status':len(notas),'aluno':aluno_})
        else:
            return render(request, 'menu/visualizar_nota.html', {'notas': notas,'status':len(notas),'aluno':aluno_})
        notas = nota.objects.filter(aluno=id , disciplina = disci) 
    
    return render(request, 'menu/visualizar_nota.html', {'notas': notas,'status':len(notas),'aluno':aluno_})


def desempenho_disciplina(request):
    lista = []
    user_name = request.user
    usuario = user.objects.get(username=user_name)
    pessoa_ = pessoa.objects.get(usuario=str(usuario.id))
    professor_ = professor.objects.get(pessoa=str(pessoa_.id))
    disciplinas = disciplina.objects.filter(professor=str(professor_.id))
    for n in range(0, len(disciplinas)):
        turmas = turma_tem_disciplina.objects.filter(
            disciplina=str(disciplinas[n].id))
        for m in range(0, len(turmas)):
            print(turmas[m])
            lista.append(turmas[m])
    return render(request, 'menu/desempenho_disciplinas.html', {'disciplinas': lista})


def desempenho_disciplina_unica (request, id, disci):
    lista_notas = []
    lista_falta = []
    lista_media = []
    data = {}
    disciplinas = disciplina.objects.get(pk=disci)
    notas = nota.objects.filter(disciplina = disci).order_by("aluno")
    for n in range(0,len(notas)):
        nota_ = notas[n]
        if n == 0:
            nota_antiga = nota_
        else:
            if nota_.aluno == nota_antiga.aluno:
                media = nota_.nota + nota_antiga.nota
                media = media/2
                media_falta = nota_.falta + nota_antiga.falta
                media_falta = media_falta/2
                lista_falta.append(media_falta)
                lista_media.append(media)
                
                if media >= 60:
                    data['aluno'] = nota_.aluno
                    data['media'] = media
                    data['faltas'] = media_falta
                    data['status'] = "Aprovado"
                else:
                    data['aluno'] = nota_.aluno
                    data['media'] = media
                    data['faltas'] = media_falta
                    data['status'] = "Reprovado"
                lista_notas.append(dict(data))
            else:
                nota_antiga = nota_
                continue
        media_geral = 0
    for n in range(len(lista_media)):
        media_geral += lista_media[n]
    
    media_geral = media_geral/len(lista_media)
    moda = statistics.mode(lista_media)
    mediana = statistics.median(lista_media)
    print(lista_media)
    return render(request, 'menu/desempenho_disciplinas_grafico.html',{'lista_falta':lista_falta,'lista_media':lista_media,'notas':notas,'disciplinas':disciplinas,"lista_notas":lista_notas,'media_geral':media_geral,'moda':moda,'mediana':mediana})