from django.contrib import admin
from .logic import threadProcessarFace
from threading import Thread

# Register your models here.
from .models import Pessoa, Acesso, Totem
from autenticacao.models import Empresa

#those models will apear in django admin panel
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportMixin, ExportActionMixin

class PessoaResource(resources.ModelResource):
    class Meta:
        model = Pessoa

#class PessoaAdmin(ImportExportModelAdmin):
class PessoaAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PessoaResource
    list_display = ('id', 'nome', 'foto_valida', 'ativo')
    fields = ('nome', 'foto', 'foto_valida', 'data_nascimento', 'genero', 'ativo')
    readonly_fields = ('foto_valida',)
    exclude = ('face_encoded', 'fkEmpresa', 'created_by', 'updated_by',)

    list_filter = ('foto_valida', 'ativo', )
    search_fields = ('nome', )

    def save_model(self, request, obj, form, change):
        if not change:
            #new object
            obj.created_by = request.user
            obj.updated_by = request.user
            obj.fkEmpresa = request.user.funcionario.fkEmpresa
        else:
            #update object
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)
        threadProcessarFace(obj)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(
                fkEmpresa=request.user.funcionario.fkEmpresa)


admin.site.register(Pessoa, PessoaAdmin)


class TotemAdmin(admin.ModelAdmin):
    class Meta:
        model = Totem

    fields = ('nome', 'descricao', 'ativo', 'user',)
    list_display = ('id', 'nome',)

    def save_model(self, request, obj, form, change):
        if not change:
            #new object
            obj.created_by = request.user
            obj.updated_by = request.user
            obj.fkEmpresa = request.user.funcionario.fkEmpresa
        else:
            #update object
            obj.updated_by = request.user

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        elif request.user.groups.filter(name = 'Administrador').exists():
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(
                user__funcionario__fkEmpresa=request.user.funcionario.fkEmpresa)


admin.site.register(Totem, TotemAdmin)

from import_export.fields import Field
from import_export.widgets import DateWidget

class AcessoResource(resources.ModelResource):
    class Meta:
        model = Acesso


class AcessoAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AcessoResource
    list_display = ('data', 'genero', 'idade')
    list_filter = ('data', 'fkTotem')
    search_fields = ('data', )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(
                fkTotem__user__funcionario__fkEmpresa=request.user.funcionario.fkEmpresa)

admin.site.register(Acesso, AcessoAdmin)