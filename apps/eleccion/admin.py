from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
#
from .models import Eleccion, Cargo, Candidato
# Register your models here.


class EleccionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title',
                    'slug',
                    'date', 'start_time', 'end_time',
                    'status',
                    'padron',
                    'cargo'
                    )
    fields = ('title', 'date', 'start_time', 'end_time',
              'status', 'padron',)


admin.site.register(Eleccion, EleccionAdmin)


#
class CargoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Cargo, CargoAdmin)


#
class CandidatoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'postulation_date')


admin.site.register(Candidato, CandidatoAdmin)
