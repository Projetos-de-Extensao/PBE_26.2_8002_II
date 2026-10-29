from django.contrib import admin

from .models import Aluno, FilaEspera, Profissional, Responsavel, Sala

# Register your models here.
admin.site.register(Sala)
admin.site.register(Aluno)
admin.site.register(Profissional)
admin.site.register(Responsavel)
admin.site.register(FilaEspera)
