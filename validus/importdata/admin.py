from django.contrib import admin

from .models import TimeSeries


@admin.register(TimeSeries)
class TimeSeriesAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']
