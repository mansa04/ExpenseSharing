from django.contrib import admin
from . models import Group, Member, Expense, ExpenseCategory

# Register your models here.
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
