from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import CompanyConfig


@admin.register(CompanyConfig)
class CompanyConfigAdmin(SingletonModelAdmin):
    pass
