from django.contrib import admin
from .models import  FilaEspera, FilaEspera, Sala, Aluno
# Register your models here.
admin.site.register(Sala)
admin.site.register(Aluno)
admin.site.register(FilaEspera)