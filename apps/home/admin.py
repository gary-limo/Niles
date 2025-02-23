# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import DataQualityCheck

@admin.register(DataQualityCheck)
class DataQualityCheckAdmin(admin.ModelAdmin):
    list_display = ('database_name', 'schema_name', 'table_name', 'column_name', 'rule_type', 'created_at')
    search_fields = ('database_name', 'schema_name', 'table_name', 'column_name')
    list_filter = ('rule_type', 'execution_frequency', 'business_critical', 'active_flag')
