from django.contrib import admin

# Register your models here.
from .models import Pessoa, Acesso

'''class EmpresaAdmin(admin.ModelAdmin):
	list_display = ['razaosocial', 'cnpj']
	search_fields = ['razaosocial', 'cnpj']

admin.site.register(Empresa, EmpresaAdmin)'''

#those models will apear in django admin panel
admin.site.register(Pessoa)
admin.site.register(Acesso)