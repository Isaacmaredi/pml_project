from django.test import TestCase

# Create your tests here.

# Update member Acccounts code snippets

from django.db import models

class MemberAccount(models.Model):
    acc_date = models.DateField()
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def update_opening_balance(self):
        # Get the last month's MemberAccount object
        last_month_account = MemberAccount.objects.filter(pk__lt=self.pk).order_by('-pk').first()

        # If there is a last month's account, update the opening_balance of the current account
        if last_month_account:
            self.opening_balance = last_month_account.closing_balance
            self.save()


# Using django signals to update closing balance 

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=MemberAccount)
def update_member_account(sender, instance, created, **kwargs):
    if created:
        instance.update_opening_balance()
