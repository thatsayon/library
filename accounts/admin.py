from django.contrib import admin
from .models import UserAccount, BorrowBook

admin.site.register(UserAccount)
admin.site.register(BorrowBook)