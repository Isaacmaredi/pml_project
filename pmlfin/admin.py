from django.contrib import admin
from .models import MemberAccount, Cashflow, Company, Share, Wealth, Co

# Register your models here

class MemberAccountAdmin(admin.ModelAdmin):
    list_display = ['name','date', 'balance_brought_forward',
                    'premiums','funeral_topup','transport_topup',
                    'fines','total_debits','cash_deposit',
                    'adjustments','total_receipts',
                    'net_movement','total_outstanding']
    
    list_editable = ('date','balance_brought_forward',
                    'premiums','funeral_topup','transport_topup',
                    'fines','cash_deposit','adjustments')

    list_display_links = ('name',)
    list_filter = ('name','date')
    list_per_page = 20
    
admin.site.register(MemberAccount, MemberAccountAdmin)

class CashflowAdmin(admin.ModelAdmin):
    list_display = ['date','opening_bank_bal','expenses','income','closing_bank_bal']
    list_editable = ('opening_bank_bal','expenses','income','closing_bank_bal')
    list_display_links = ('date',)
    list_filter = ('date',)
    list_per_page = 20
    
admin.site.register(Cashflow, CashflowAdmin)

admin.site.register(Company)

admin.site.register(Share)

admin.site.register(Wealth)

admin.site.register(Co)


    


