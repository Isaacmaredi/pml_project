from django.contrib import admin
from .models import Profile, Beneficiary

# Register your models here.
class ProfileAdmin (admin.ModelAdmin):
    list_display = ['id', 'user','shortname', 'birth_date',
                    'status','status_date','address','province']
    list_display_links = ('id','user')
    list_fiter = ('province')
    search_fields = ('user__username',)
    list_per_page = 20
    
admin.site.register(Profile, ProfileAdmin)
    
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ['member','name','beneficiary_type','birth_date',
                    'beneficiary_status','is_paid','paid_date']
    list_display_links = ('name',)
    list_fiter = ('name','member')
    search_fields = ('name','member')
    list_per_page = 25
    
admin.site.register(Beneficiary, BeneficiaryAdmin)

    
    