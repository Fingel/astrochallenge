from django.contrib import admin
from django.db import models
from django_markdown.admin import AdminMarkdownWidget
from models import Challenge, CompletedChallenge


class ChallengeAdmin(admin.ModelAdmin):
    filter_horizontal = ('astroobjects', 'solarsystemobjects')
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownWidget}
    }


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(CompletedChallenge)
