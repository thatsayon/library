from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2) 

    def __str__(self):
        return str(self.account_no)

class BorrowBook(models.Model):
    user = models.ForeignKey(UserAccount, related_name='borrowbook', on_delete=models.CASCADE)
    bookid = models.IntegerField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} borrow the book with id: {self.bookid}")