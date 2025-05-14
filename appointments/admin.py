from django.contrib import admin
from .models import Appointment, AppointmentItem


class AppointmentItemInline(admin.TabularInline):
    model = AppointmentItem
    extra = 1


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 
                    'created_at')
    search_fields = ('first_name', 'last_name')
    list_filter = ('created_at',)
    inlines = [AppointmentItemInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'first_name', 'last_name',
                       'middle_name', 'phone_number')
        }),
    )


admin.site.register(Appointment, AppointmentAdmin)