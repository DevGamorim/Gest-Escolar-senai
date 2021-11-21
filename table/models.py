from django.contrib.auth.models import AbstractUser
from django.db import models


class user(AbstractUser):
    privilegio = (
        ('adm', 'Administrador'),
        ('aluno', 'Aluno'),
        ('prof', 'Professor'),
    )
    privilegio = models.CharField(
        max_length=5,
        choices=privilegio,
    )


class endereco(models.Model):
    id = models.AutoField(primary_key=True)
    bairro = models.CharField(max_length=100)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=100, unique=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class pessoa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    nascimento = models.DateField()
    endereco = models.ForeignKey(endereco, on_delete=models.CASCADE)
    usuario = models.ForeignKey(user, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class professor(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class disciplina(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    carga_horaria = models.IntegerField()
    professor = models.ForeignKey(professor, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class aluno(models.Model):
    id = models.AutoField(primary_key=True)
    pessoa = models.ForeignKey(pessoa, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class nota(models.Model):
    id = models.AutoField(primary_key=True)
    bimestre = models.IntegerField()
    falta = models.IntegerField()
    nota = models.FloatField()
    aluno = models.ForeignKey(aluno, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(disciplina, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class turma(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    semestre = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class turma_tem_disciplina(models.Model):
    id = models.AutoField(primary_key=True)
    disciplina = models.ForeignKey(disciplina, on_delete=models.CASCADE)
    turma = models.ForeignKey(turma, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class turma_tem_aluno(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(turma, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class curso(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    tipo = models.IntegerField(unique=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class turma_tem_curso(models.Model):
    id = models.AutoField(primary_key=True)
    turma = models.ForeignKey(turma, on_delete=models.CASCADE)
    curso = models.ForeignKey(curso, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
