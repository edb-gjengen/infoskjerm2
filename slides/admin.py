from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from slides.models import Slide


class SlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'url', 'status', 'activate_date', 'deactivate_date']
    ordering = ['order', 'status', '-activate_date']

admin.site.register(Slide, SlideAdmin)
