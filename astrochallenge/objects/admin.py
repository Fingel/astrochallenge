from django.contrib import admin
from astrochallenge.objects.models import AstroObject, CatalogObject

admin.site.register(AstroObject)
admin.site.register(CatalogObject)
