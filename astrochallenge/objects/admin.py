from django.contrib import admin
from astrochallenge.objects.models import AstroObject, CatalogObject, Constellation

admin.site.register(AstroObject)
admin.site.register(CatalogObject)
admin.site.register(Constellation)
