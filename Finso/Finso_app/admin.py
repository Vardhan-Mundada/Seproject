from django.contrib import admin
from .models import Category, Expense, RecurringExpense, Income

admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(RecurringExpense)
admin.site.register(Income)
# Register your models here.
