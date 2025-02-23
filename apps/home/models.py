# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DataQualityCheck(models.Model):
    FREQUENCY_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    RULE_TYPE_CHOICES = [
        ('LENGTH_CHECK', 'Length Check'),
        ('NULL_OR_EMPTY_CHECK', 'Null or Empty Check'),
        ('ALPHABET_CHECK', 'Alphabet Check'),
        ('PATTERN_MATCHING', 'Pattern Matching'),
        ('PK_CHECK', 'Primary Key Check'),
        ('TIMESTAMP_CONSISTENCY_CHECK', 'Timestamp Consistency Check'),
        ('HASHKEY_ACCURACY_CHECK', 'Hashkey Accuracy Check'),
        ('CUSTOM_SQL', 'Custom SQL'),
    ]

    BUSINESS_CRITICAL_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    # Auto-incrementing ID
    id = models.AutoField(primary_key=True)

    # Required fields
    database_name = models.CharField(max_length=255)
    schema_name = models.CharField(max_length=255)
    table_name = models.CharField(max_length=255)
    column_name = models.CharField(max_length=255)
    rule_type = models.CharField(max_length=50, choices=RULE_TYPE_CHOICES)
    execution_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    alert_recipient = models.EmailField()
    business_critical = models.CharField(max_length=3, choices=BUSINESS_CRITICAL_CHOICES)
    active_flag = models.IntegerField(choices=[(0, '0'), (1, '1')])

    # Optional fields (nullable)
    second_column = models.CharField(max_length=255, null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    operator = models.CharField(max_length=10, null=True, blank=True)
    start_value = models.CharField(max_length=255, null=True, blank=True)
    end_value = models.CharField(max_length=255, null=True, blank=True)
    values = models.TextField(null=True, blank=True)  # For comma-separated values
    threshold_value = models.CharField(max_length=255, null=True, blank=True)
    like_pattern = models.CharField(max_length=255, null=True, blank=True)
    custom_sql = models.TextField(null=True, blank=True)

    # Timestamps for tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_quality_checks'
        verbose_name = 'Data Quality Check'
        verbose_name_plural = 'Data Quality Checks'

    def __str__(self):
        return f"{self.database_name}.{self.schema_name}.{self.table_name} - {self.rule_type}"

    def save(self, *args, **kwargs):
        # Ensure active_flag is either 0 or 1
        if self.active_flag not in [0, 1]:
            self.active_flag = 1
        super().save(*args, **kwargs)

