from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = "pages"

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),

    path('perfil/criar/', views.criar_user, name='perfil_criar_user'),
    path('perfil/', views.perfil, name='perfil'),

    path('notas/lancamento/', views.lancamento_nota, name='lancamento_nota'),

    path('novo/disciplina/', views.nova_disciplina, name='novo_disciplina'),

    path('turmas/criar/', views.criar_turma, name='criar_turma'),

    path('turmas/adicionar/disciplina/', views.adicionar_diciplica_a_turma,
         name='adicionar_diciplica_a_turma'),

    path('turmas/adicionar/alunos/', views.adicionar_turma_tem_aluno,
         name='adicionar_turma_tem_aluno'),

    path('turmas/adicionar/cursos/', views.criar_turma_tem_curso,
         name='criar_turma_tem_curso'),
]
