from django.contrib import admin
from .models import Profile, Beneficiary, Committee

# Register your models here.
class ProfileAdmin (admin.ModelAdmin):
    list_display = ['id', 'user','shortname', 'birth_date',
                    'status','status_date','address','province']
    list_display_links = ('id','user')
    list_filter = ('province',)
    search_fields = ('user__username',)
    list_per_page = 20
    
admin.site.register(Profile, ProfileAdmin)
    
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ['member','name','beneficiary_type',
                    'beneficiary_status','is_paid','paid_date']
    list_display_links = ('name',)
    list_filter = ('beneficiary_type', 'beneficiary_status','member')
    search_fields = ('member',)
    list_per_page = 25
    
admin.site.register(Beneficiary, BeneficiaryAdmin)

class CommitteeAdmin(admin.ModelAdmin):
    list_filter = ('name',)

admin.site.register(Committee, CommitteeAdmin)