from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from datetime import date
from django.utils.timezone import now


class DateLimitedActivatorQuerySet(models.query.QuerySet):
    def get_date_query(self):
        today = date.today()
        return (
            Q(activate_date__lte=today, deactivate_date__isnull=True)
            | Q(activate_date__lte=today, deactivate_date__gte=today))

    def active(self):
        """ Returns active query set """
        return self.filter(status=Slide.ACTIVE_STATUS).filter(self.get_date_query())

    def inactive(self):
        """ Returns inactive query set """
        return self.filter(Q(status=Slide.INACTIVE_STATUS) | Q(~self.get_date_query()))


class DateLimitedActivatorModelManager(models.Manager):
    def get_queryset(self):
        """ Use DateLimitedActivatorQuerySet for all results """
        return DateLimitedActivatorQuerySet(model=self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()


class Slide(TimeStampedModel, models.Model):
    """Slide model"""
    INACTIVE_STATUS, ACTIVE_STATUS = range(2)
    STATUS_CHOICES = (
        (INACTIVE_STATUS, _('Inactive')),
        (ACTIVE_STATUS, _('Active')),
    )

    url = models.URLField(_('url'))
    title = models.CharField(_('title'), max_length=254, blank=True)
    activate_date = models.DateField(
        _('activate date'),
        blank=True,
        help_text=_('keep empty for an immediate activation'))
    deactivate_date = models.DateField(
        _('deactivate date'),
        blank=True,
        null=True,
        help_text=_('keep empty for indefinite activation'))
    order = models.PositiveIntegerField(_('order'), default=0)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=ACTIVE_STATUS)
    objects = DateLimitedActivatorModelManager()

    # thumbnail = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ('order', 'status')

    def save(self, *args, **kwargs):
        if not self.activate_date:
            self.activate_date = now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url
