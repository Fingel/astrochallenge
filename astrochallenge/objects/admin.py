from django.contrib import admin
from astrochallenge.objects.models import AstroObject, CatalogObject, Constellation, SolarSystemObject, Observation


class AstroObjectAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'catalog_rep')
    list_filter = ('type', 'constellation')
    search_fields = ('common_name', 'description')


class SolarSystemObjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('type',)
    search_fields = ('name', 'description')

admin.site.register(AstroObject, AstroObjectAdmin)
admin.site.register(CatalogObject)
admin.site.register(Constellation)
admin.site.register(Observation)
admin.site.register(SolarSystemObject, SolarSystemObjectAdmin)
