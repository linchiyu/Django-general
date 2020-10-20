from django.contrib import admin
import re
# Register your models here.
from .models import Server, Camera

'''class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['razaosocial', 'cnpj']
    search_fields = ['razaosocial', 'cnpj']

admin.site.register(Empresa, EmpresaAdmin)'''

#those models will apear in django admin panel
class CameraAdmin(admin.ModelAdmin):
    class Meta:
        model = Camera
    list_display = ['id', 'name', 'active']
    search_fields = ['name', 'active']
    list_filter = ['active']
    fields = ('name', 'configuration', 'active', 'fkserver')
    #exclude = ('memory_name',)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        obj.memory_name = re.sub('[^A-Za-z0-9_]+', '', obj.name +'_'+ str(obj.id))
        super().save_model(request, obj, form, change)


admin.site.register(Server)
admin.site.register(Camera, CameraAdmin)
#admin.site.unregister(Camera, CameraAdmin)

'''
from import_export import resources
from import_export.admin import ImportExportModelAdmin
class PessoaResource(resources.ModelResource):
    class Meta:
        model = Pessoa
class PessoaAdmin(ImportExportModelAdmin):
    resource_class = PessoaResource
admin.site.register(Pessoa, PessoaAdmin)
'''

