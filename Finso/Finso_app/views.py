from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

# Expense category

from .models import Category
from .forms import CategoryForm


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'category_list.html', {'categories': categories, 'form': form})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'edit_category.html', {'form': form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')

    return render(request, 'delete_category.html', {'category': category})




#Expense Transaction

from .models import Expense
from .forms import ExpenseForm

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')

    return render(request, 'delete_expense.html', {'expense': expense})




#Graph plotting

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import matplotlib.pyplot as plt
from io import BytesIO
import base64


@login_required
def expense_statistics(request):
    expenses = Expense.objects.filter(user=request.user)
    categories = expenses.values_list('category__name', flat=True).distinct()

    # Paginate the categories
    paginator = Paginator(categories, 5)  # Show 5 categories per page
    page = request.GET.get('page')

    try:
        categories_page = paginator.page(page)
    except PageNotAnInteger:
        categories_page = paginator.page(1)
    except EmptyPage:
        categories_page = paginator.page(paginator.num_pages)

    # Get the selected categories for the current page
    selected_categories = categories_page.object_list

    # Create pie chart
    pie_chart = create_pie_chart(request.user, selected_categories)

    # Create bar chart
    bar_chart = create_bar_chart(request.user, selected_categories)

    context = {
        'categories_page': categories_page,
        'pie_chart': pie_chart,
        'bar_chart': bar_chart,
    }

    return render(request, 'expense_statistics.html', context)

def create_pie_chart(user, selected_categories):
    expenses = Expense.objects.filter(user=user, category__name__in=selected_categories)
    category_totals = {category: 0 for category in selected_categories}

    for expense in expenses:
        category_totals[expense.category.name] += expense.amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    # Plotting pie chart with size (5, 5)
    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution by Category')

    # Save the chart to BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the image to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close()  # Close the figure to free up resources

    return image_base64

def create_bar_chart(user, selected_categories):
    expenses = Expense.objects.filter(user=user, category__name__in=selected_categories)
    category_totals = {category: 0 for category in selected_categories}

    for expense in expenses:
        category_totals[expense.category.name] += expense.amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    # Plotting bar chart with size (10, 5)
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Total Expense Amount')
    plt.title('Total Expense Amount by Category')

    # Save the chart to BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the image to base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close()  # Close the figure to free up resources

    return image_base64