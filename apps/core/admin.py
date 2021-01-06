from django.contrib import admin
# inport/export tables from db
from import_export import resources
# costom admin for Users
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
#
from .models import (Eleccion,
                     Elector,
                     Cargo,
                     Candidato,
                     Padron,
                     Sufragio)


# Register your models here.


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin, ExportMixin, UserAdmin):
    list_display = ('username', 'is_staff', 'is_active', 'date_joined', )
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#


class EleccionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title',
                    'slug',
                    'date', 'start_time', 'end_time',
                    'eleccion_estatus',
                    'eleccion_padron',
                    'eleccion_cargo'
                    )
    fields = ('title', 'date', 'start_time', 'end_time',
              'eleccion_estatus', 'eleccion_padron',)
    # ,


admin.site.register(Eleccion, EleccionAdmin)


class ElectorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'dni', 'names', 'surnames', 'user')


admin.site.register(Elector, ElectorAdmin)
#


class CargoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Cargo, CargoAdmin)
#


class CandidatoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'postulation_date')


admin.site.register(Candidato, CandidatoAdmin)
#


class PadronAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'date')
    fields = ('title', 'date')


admin.site.register(Padron, PadronAdmin)

#


class SufragioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('hash', 'voting_time')


admin.site.register(Sufragio, SufragioAdmin)
