# forms.py
from django import forms
from .models import Category
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'content']

    widgets = {
        'amount': forms.NumberInput(attrs={'step': '0.01'}),
        'category': forms.Select(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
    }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'budget_limit']



