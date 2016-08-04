from django.db import models
from django.db.models import Q

from django_extensions.db.models import TimeStampedModel, ActivatorModel, ActivatorModelManager, ActivatorQuerySet
from datetime import date


class DateLimitedActivatorQuerySet(ActivatorQuerySet):
    def get_date_query(self):
        today = date.today()
        return (
            Q(start__isnll=True, stop__isnull=True)
            | Q(start__gte=today, stop__lte=today)
            | Q(start__gte=today, stop__isnull=True)
            | Q(start__isnll=True, stop__lte=today)
        )

    def active(self):
        """ Returns active query set """
        return self.filter(status=DateLimitedActivatorModelManager.ACTIVE_STATUS).filter(self.get_date_query())

    def inactive(self):
        """ Returns inactive query set """
        return self.filter(status=DateLimitedActivatorModelManager.INACTIVE_STATUS).filter(Q(~self.get_date_query()))


class DateLimitedActivatorModelManager(ActivatorModelManager):
    def get_queryset(self):
        """ Use ActivatorQuerySet for all results """
        return DateLimitedActivatorQuerySet(model=self.model, using=self._db)


class Slide(TimeStampedModel, ActivatorModel):
    url = models.URLField()
    title = models.CharField(max_length=254, blank=True)
    # thumbnail = models.ImageField(blank=True, null=True)
    start = models.DateField(blank=True, null=True)
    stop = models.DateField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

