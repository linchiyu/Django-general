from django.contrib import admin

from .models import Satisfacao

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ExportMixin

# Register your models here.

class SatisfacaoResource(resources.ModelResource):
    class Meta:
        model = Satisfacao

class SatisfacaoAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SatisfacaoResource
    list_display = ('data', 'emocao',)
    list_filter = ('data', )
    search_fields = ('data', )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(
                fkTotem__user__funcionario__fkEmpresa=request.user.funcionario.fkEmpresa)

admin.site.register(Satisfacao, SatisfacaoAdmin)
