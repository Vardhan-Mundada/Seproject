from django.contrib import admin
from .models import Category, Expense, RecurringExpense

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(RecurringExpense)
# Register your models here.
