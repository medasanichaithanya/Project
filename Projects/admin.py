from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.
class InformationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(Information, InformationAdmin)
