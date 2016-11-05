from django.contrib import admin
from personas.models import *
from django.contrib.auth.models import Permission


class UsuarioAdmin(admin.ModelAdmin):
    pass


class PersonaAdmin(admin.ModelAdmin):
    pass


class EmpleadoAdmin(admin.ModelAdmin):
    pass


class DueniaAdmin(admin.ModelAdmin):
    pass


class ClienteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Persona,PersonaAdmin)
admin.site.register(Empleado,EmpleadoAdmin)
admin.site.register(Duenia,DueniaAdmin)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Permission)