from django.db import models
from django.urls import reverse

from model_utils.models import TimeStampedModel


class TimeSeries(TimeStampedModel):
    # sheet_name = models.CharField(max_length=256, unique=True)
    valuation_date = models.DateField(blank=True, null=True)
    underlying = models.CharField(max_length=16, blank=True)
    mid = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.underlying + ' ' + str(self.valuation_date) + ' ' + \
            str(self.mid)

    def get_absolute_url(self):
        # return reverse('upload', kwargs={'pk': self.pk})
        return reverse('importdata:upload')


# class SheetName(TimeStampedModel):
#     name = models.CharField(max_length=256)
#
#     def __unicode__(self):
#         return self.name
