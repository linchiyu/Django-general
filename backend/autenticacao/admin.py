from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Funcionario
from .models import Empresa
# Register your models here.
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class FuncionarioInline(admin.StackedInline):
    model = Funcionario
    can_delete = False
    verbose_name_plural = 'funcionarios'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (FuncionarioInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Empresa)
