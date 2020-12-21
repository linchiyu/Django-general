from django.contrib import admin

from .models import FaixaEtaria, Propaganda
from autenticacao.models import Empresa
# Register your models here.


from import_export import resources
from import_export.admin import ImportExportModelAdmin

class FaixaEtariaAdmin(admin.ModelAdmin):
    class Meta:
        model = FaixaEtaria

    list_display = ('nome', 'idade_minima', 'idade_maxima')

    '''def has_add_permission(self, request): 
        return False

    def has_delete_permission(self, request, obj=None): 
        return False

    def has_change_permission(self, request, obj=None): 
        return False'''


class PropagandaAdmin(admin.ModelAdmin):
    class Meta:
        model = Propaganda

    list_display = ('nome', 'imagem')
    
    #readonly_fields = ['created_by', 'updated_by']

    exclude = ['created_by', 'updated_by', 'fkEmpresa']


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

    #mostrar apenas querysets da empresa do usuario
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(fkEmpresa=request.user.funcionario.fkEmpresa)

admin.site.register(FaixaEtaria, FaixaEtariaAdmin)
admin.site.register(Propaganda, PropagandaAdmin)