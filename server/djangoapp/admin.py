from django.contrib import admin
from import_export import resources
from .models import CarModel, CarMake
from import_export.admin import ImportExportModelAdmin

class CarMakeResource(resources.ModelResource):
    class Meta:
        model = CarMake

class CarModelResource(resources.ModelResource):
    class Meta:
        model = CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3


class CarModelAdmin(ImportExportModelAdmin):
    list_display = ('dealer_id', 'name', 'carMakeName', 'type', 'year')
    search_fields = ['name', 'dealer_id', 'type']


class CarMakeAdmin(ImportExportModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description', 'establish_date')
    search_fields = ['name', 'description']


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
