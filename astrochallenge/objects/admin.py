from django.contrib import admin
from astrochallenge.objects.models import AstroObject, CatalogObject, Constellation, SolarSystemObject, Observation

admin.site.register(AstroObject)
admin.site.register(CatalogObject)
admin.site.register(Constellation)
admin.site.register(Observation)
admin.site.register(SolarSystemObject)
