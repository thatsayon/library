from django.db import models
from accounts.models import UserAccount

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    balance_after = models.DecimalField(decimal_places=2, max_digits=7)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']