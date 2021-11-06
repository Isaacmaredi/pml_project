from django.contrib import admin
from .models import Meeting, Attendance, Funeral, FuneralAttendance
# Register your models here.
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['id','date','meeting_type','host','alt_venue']
    list_filter = ('date',)
    search_fields = ('host',)
    list_per_page = 15

admin.site.register(Meeting, MeetingAdmin)

class FuneralAdmin(admin.ModelAdmin):
    list_display = ['id','date','bereaved_member','deceased_type','deceased_member','deceased_beneficiary','venue']
    list_filter = ('date','deceased_type','bereaved_member')
    search_fields = ('bereaved_member','deceased_type','deceased_beneficiary')
    list_per_page = 15

admin.site.register(Funeral, FuneralAdmin)

# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ['meeting']

# admin.site.register(Attendance, AttendanceAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['meeting','member','is_present','absence_reason']
    list_filter = ('meeting','is_present')
    search_fields = ('meeting',)
    list_editable = ('is_present','absence_reason',)
    
admin.site.register(Attendance, AttendanceAdmin)

class FuneralAttendanceAdmin(admin.ModelAdmin):
    list_display = ['funeral','member','is_present','absence_reason']
    list_filter = ('funeral','is_present',)
    search_fields = ('funeral','member',)
    list_editable = ('is_present','absence_reason',)

admin.site.register(FuneralAttendance, FuneralAttendanceAdmin)

    
    