from django.contrib import admin
from .models import Meeting, Attendance
# Register your models here.
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['id','date','meeting_type','host','alt_venue']
    list_filter = ('date',)
    search_fields = ('host',)
    list_per_page = 15

admin.site.register(Meeting, MeetingAdmin)

# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ['meeting']

# admin.site.register(Attendance, AttendanceAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['meeting','member','is_present','absence_reason']
    list_filter = ('meeting','is_present')
    search_fields = ('meeting',)
    list_editable = ('is_present',)
    
admin.site.register(Attendance, AttendanceAdmin)

    
    