from django.contrib import admin
from .logic import encodeFace
from threading import Thread

# Register your models here.
from .models import Pessoa, Acesso, Totem
from autenticacao.models import Empresa

#those models will apear in django admin panel
admin.site.register(Acesso)

from import_export import resources
from import_export.admin import ImportExportModelAdmin

#call  t = Thread(target=processarFace, args=(novaPessoa,), daemon=True).start()
def processarFace(pessoa):
    encoded = encodeFace(pessoa.foto)
    pessoa.face_encoded = encoded
    if len(encoded) > 300:
    	pessoa.foto_valida = True
    pessoa.save()

class PessoaResource(resources.ModelResource):
    class Meta:
        model = Pessoa

class PessoaAdmin(ImportExportModelAdmin):
    resource_class = PessoaResource
    #fields = ('nome', 'foto', 'data_nascimento', 'genero', 'ativo')

    
    def save_model(self, request, obj, form, change):
        if not change:
            #new object
            obj.created_by = request.user
            obj.updated_by = request.user
            obj.fkEmpresa = request.user.funcionario.fkEmpresa
        else:
            #updating object
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)
        t = Thread(target=processarFace, args=(obj,), daemon=True).start()


admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Totem)