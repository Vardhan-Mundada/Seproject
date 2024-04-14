from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def profile(request):
    return render(request, 'profile.html')

def addall(request):
    return render(request, 'addall.html')

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


from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


#signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Website!'
        message = 'Thank you for creating an account.'
        from_email = settings.EMAIL_HOST_USER
        to_email = [instance.email]
        send_mail(subject, message, from_email, to_email)
        create_categories(instance)

def create_categories(user):
    Category.objects.create(user=user, name='education', budget_limit=1000)
    Category.objects.create(user=user, name='grocery', budget_limit=2000)
    Category.objects.create(user=user, name='shoppind', budget_limit=3000)

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

    return render(request, 'add_category.html', {'form': form, 'categories':categories})

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

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64


# @login_required
# def expense_statistics(request):
#     expenses = Expense.objects.filter(user=request.user)
#     categories = expenses.values_list('category__name', flat=True).distinct()

#     # Paginate the categories
#     paginator = Paginator(categories, 20)  # Show 5 categories per page
#     page = request.GET.get('page')

#     try:
#         categories_page = paginator.page(page)
#     except PageNotAnInteger:
#         categories_page = paginator.page(1)
#     except EmptyPage:
#         categories_page = paginator.page(paginator.num_pages)

#     # Get the selected categories for the current page
#     selected_categories = categories_page.object_list

#     # Create pie chart
#     pie_chart = create_pie_chart(request.user, selected_categories)

#     # Create bar chart
#     bar_chart = create_bar_chart(request.user, selected_categories)

#     context = {
#         'categories_page': categories_page,
#         'pie_chart': pie_chart,
#         'bar_chart': bar_chart,
#     }

#     return render(request, 'expense_statistics.html', context)

# def create_pie_chart(user, selected_categories):
#     expenses = Expense.objects.filter(user=user, category__name__in=selected_categories)
#     category_totals = {category: 0 for category in selected_categories}

#     for expense in expenses:
#         category_totals[expense.category.name] += expense.amount

#     labels = list(category_totals.keys())
#     values = list(category_totals.values())

#     # Plotting pie chart with size (5, 5)
#     plt.figure(figsize=(5, 5))
#     plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
#     plt.title('Expense Distribution by Category')

#     # Save the chart to BytesIO buffer
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     # Encode the image to base64
#     image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

#     plt.close()  # Close the figure to free up resources

#     return image_base64

# def create_bar_chart(user, selected_categories):
#     expenses = Expense.objects.filter(user=user, category__name__in=selected_categories)
#     category_totals = {category: 0 for category in selected_categories}

#     for expense in expenses:
#         category_totals[expense.category.name] += expense.amount

#     labels = list(category_totals.keys())
#     values = list(category_totals.values())

#     # Plotting bar chart with size (10, 5)
#     plt.figure(figsize=(10, 5))
#     plt.bar(labels, values, color='blue')
#     plt.xlabel('Categories')
#     plt.ylabel('Total Expense Amount')
#     plt.title('Total Expense Amount by Category')

#     # Save the chart to BytesIO buffer
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     # Encode the image to base64
#     image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

#     plt.close()  # Close the figure to free up resources

#     return image_base64



# duration graph
# from django.utils import timezone
# import base64
# from io import BytesIO
# import matplotlib.pyplot as plt


# @login_required
# def expense_statistics2(request):
#     time_interval = request.GET.get('time_interval', 'weekly')  # Default to weekly if not specified
#     end_date = timezone.now().date()
#     if time_interval == 'weekly':
#         start_date = end_date - timezone.timedelta(days=7)
#     elif time_interval == 'monthly':
#         start_date = end_date - timezone.timedelta(days=30)  # Approximate 30 days as a month
#     elif time_interval == '3_months':
#         start_date = end_date - timezone.timedelta(days=90)  # 3 months
#     elif time_interval == '6_months':
#         start_date = end_date - timezone.timedelta(days=180)  # 6 months
#     elif time_interval == 'yearly':
#         start_date = end_date - timezone.timedelta(days=365)  # 1 year
#     else:
#         # Handle other intervals if needed
#         start_date = end_date

#     expenses = Expense.objects.filter(user=request.user, date__range=[start_date, end_date])
#     categories = expenses.values_list('category__name', flat=True).distinct()

#     pie_chart = create_pie_chart(request.user, categories, expenses)
#     bar_chart = create_bar_chart(request.user, categories, expenses)

#     context = {
#         'time_interval': time_interval,
#         'categories': categories,
#         'pie_chart': pie_chart,
#         'bar_chart': bar_chart,
#     }

#     return render(request, 'expense_statistics2.html', context)

# def create_pie_chart(user, categories, expenses):
#     category_totals = {category: 0 for category in categories}

#     for expense in expenses:
#         category_totals[expense.category.name] += expense.amount

#     labels = list(category_totals.keys())
#     values = list(category_totals.values())

#     plt.figure(figsize=(5, 5))
#     plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
#     plt.title('Expense Distribution by Category')

#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

#     plt.close()

#     return image_base64

# def create_bar_chart(user, categories, expenses):
    category_totals = {category: 0 for category in categories}

    for expense in expenses:
        category_totals[expense.category.name] += expense.amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Total Expense Amount')
    plt.title('Total Expense Amount by Category')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close()

    return image_base64


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import base64
from io import BytesIO
from django.db.models import Q
from .models import Expense
from django.db.models.functions import Coalesce, Cast
from django.db.models import Sum, DecimalField, F, Value

@login_required
def expense_statistics(request):
    time_interval = request.GET.get('time_interval', 'weekly')  
    end_date = timezone.now().date()
    
    if time_interval == 'weekly':
        start_date = end_date - timezone.timedelta(days=7)
    elif time_interval == 'monthly':
        start_date = end_date - timezone.timedelta(days=30)  
    elif time_interval == '3months':
        start_date = end_date - timezone.timedelta(days=90)  
    elif time_interval == '6months':
        start_date = end_date - timezone.timedelta(days=180) 
    elif time_interval == 'yearly':
        start_date = end_date - timezone.timedelta(days=365) 
    else:
        start_date = end_date

    expenses = Expense.objects.filter(user=request.user, date__range=[start_date, end_date])
    categories = expenses.values_list('category__name', flat=True).distinct()

    total_income = Income.objects.filter(user=request.user).aggregate(total_income=Sum('amount'))['total_income'] or 0
    total_expenses = expenses.aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0
    remaining_amount = total_income - total_expenses

    category_totals = (
    Expense.objects.filter(user=request.user, date__range=[start_date, end_date])
    .values('category__name')
    .annotate(
        total_expenses=Coalesce(
            Cast(Sum('amount'), output_field=DecimalField()), 
            Value(0, output_field=DecimalField())
        )
    )
    .order_by('-total_expenses')[:4]
)

    # Get the 10 most recent expenses
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:7]

    pie_chart = create_pie_chart(request.user, categories, expenses)
    bar_chart = create_bar_chart(request.user, categories, expenses)

    context = {
        'time_interval': time_interval,
        'categories': categories,
        'pie_chart': pie_chart,
        'bar_chart': bar_chart,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'remaining_amount': remaining_amount,
        'recent_expenses': recent_expenses,
        'category_totals': category_totals,
    }

    return render(request, 'expense_statistics.html', context)

def create_pie_chart(user, categories, expenses):
    category_totals = {category: 0 for category in categories}

    for expense in expenses:
        category_totals[expense.category.name] += expense.amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.6))
    plt.title('Expense Distribution by Category')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close()

    return image_base64

def create_bar_chart(user, categories, expenses):
    category_totals = {category: 0 for category in categories}

    for expense in expenses:
        category_totals[expense.category.name] += expense.amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    plt.figure(figsize=(6, 5))
    plt.bar(labels, values, color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Total Expense Amount')
    plt.title('Total Expense Amount by Category')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close()

    return image_base64





#Notification of budget exceed
from django.db.models import Sum 
@login_required
def notifications(request):
    categories = Category.objects.filter(user=request.user)
    exceeded_categories = []

    for category in categories:
        total_expense = Expense.objects.filter(user=request.user, category=category).aggregate(total=Sum('amount'))['total'] or 0
        if total_expense > category.budget_limit:
            exceeded_categories.append(category)

    # Retrieve reminders for recurring expenses due today
    current_date = timezone.now().date()
    reminders = RecurringExpense.objects.filter(user=request.user, next_due_date=current_date)

    context = {
        'exceeded_categories': exceeded_categories,
        'reminders': reminders,
    }

    return render(request, 'notifications.html', context)


# Recurring bills

from .models import RecurringExpense
from .forms import RecurringExpenseForm

@login_required
def add_recurring_expense(request):
    if request.method == 'POST':
        form = RecurringExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('add_recurring_expense')
    else:
        form = RecurringExpenseForm()
    
    # Retrieve the 8 most recent recurring expenses
    recurring_expenses = RecurringExpense.objects.filter(user=request.user).order_by('-start_date')[:8]
    
    return render(request, 'add_recurring_expense.html', {'form': form, 'recurring_expenses': recurring_expenses})




#Bill detection
from .forms import ImageUploadForm
import pytesseract
from PIL import Image
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import nltk

# def billamount(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = request.FILES.get('receipt')  # Access 'receipt' field instead of 'image'
#             if image:
#                 text = extract_text_from_image(image)
#                 print(text)
#                 highest_amount = extract_highest_amount(text)
#                 category_name = categorize_bill(text)
#                 print("Highest Amount:", highest_amount)
#                 print("Category:", category_name)

#                 # Find or create the category
#                 category, _ = Category.objects.get_or_create(name=category_name)

#                 # Create the expense
#                 if highest_amount and category:
#                     expense = Expense.objects.create(
#                         user=request.user,
#                         amount=highest_amount,
#                         category=category,
#                         content=f"Expense for {category_name}"
#                     )
#                     expense.save()

#                 return render(request, 'expense_statistics.html', {'category_name': category_name, 'highest_amount': highest_amount})
#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload_receipt.html', {'form': form})

# @login_required
# def billamount(request):
#     if request.method == 'POST' and request.FILES['image']:
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = request.FILES['image']
#             text = extract_text_from_image(image)
#             print(text)
#             highest_amount = extract_highest_amount(text)
#             category_name = categorize_bill(text)
#             print("Highest Amount:", highest_amount)
#             print("Category:", category_name)

#             # Find or create the category
#             category, _ = Category.objects.get_or_create(name=category_name)

#             # Create the expense
#             if highest_amount and category:
#                 expense = Expense.objects.create(
#                     user=request.user,
#                     amount=highest_amount,
#                     category=category,
#                     content=f"Expense for {category_name}"
#                 )
#                 expense.save()

#             # return render(request, 'expense_statistics.html', {'category_name': category_name, 'highest_amount': highest_amount})
#             return redirect('expense_statistics')

#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload_receipt.html', {'form': form})


# def extract_text_from_image(image):
#     img = Image.open(image)
#     text = pytesseract.image_to_string(img)
#     return text

# def extract_highest_amount(text):
#     # Remove lines containing dates and bill numbers
#     lines = [line for line in text.split('\n') if not re.search(r'\b\d{2}\.\d{2}\.\d{4}\b|\bBill\s+No\.\s*\d+\b', line)]

#     # Extract amounts from remaining lines
#     amounts = []
#     for line in lines:
#         # Find numeric values in the line
#         nums = re.findall(r'\b\d+(?:\.\d+)?\b', line)
#         # Add numeric values to amounts list
#         amounts.extend(map(float, nums))

#     # Return the highest amount
#     if amounts:
#         return max(amounts)
#     else:
#         return None

# def categorize_bill(text):
#     nltk.download('punkt')
#     nltk.download('wordnet')

#     # Tokenize the text
#     tokens = word_tokenize(text.lower())

#     # Define categories
#     # categories = {
#     #     'entertainment': ['happy', 'restaurant', 'food', 'kitchen', 'hotel', 'room', 'park', 'movie', 'cinema', 'popcorn', 'combo meal'],
#     #     'home_utility': ['internet', 'telephone', 'electricity', 'meter', 'wifi', 'broadband', 'consumer', 'reading', 'gas', 'water', 'postpaid', 'prepaid'],
#     #     'grocery': ['bigbasket', 'milk', 'atta', 'sugar', 'sunflower', 'oil', 'bread', 'vegetable', 'fruit', 'salt', 'paneer', 'brinjal', 'tomato', 'potato'],
#     #     'investment': ['endowment', 'grant', 'loan', 'applicant', 'income', 'expenditure', 'profit', 'interest', 'expense', 'finance', 'property', 'money', 'fixed', 'deposit', 'kissan', 'vikas'],
#     #     'transport': ['car', 'cab', 'ola', 'uber', 'autorickshaw', 'railway', 'air', 'emirates', 'aerofloat', 'taxi', 'booking', 'road', 'highway'],
#     #     'shopping': ['dress', 'iphone', 'laptop', 'saree', 'max', 'pantaloons', 'westside', 'vedic', 'makeup', 'lipstick', 'cosmetics', 'mac', 'facewash', 'heels', 'crocs', 'footwear', 'purse', 'hair', 'Ribbons'],
#     #     'education':['pencil', 'pen', 'geometry', 'box', 'ink', 'pages', 'book', 'books', 'notebook', 'textbook'],

#     # }

#     categories = {
#     'entertainment': ['happy', 'restaurant', 'food', 'kitchen', 'hotel', 'room', 'park', 'movie', 'cinema', 'popcorn', 'combo meal'],
#     'home_utility': ['internet', 'telephone', 'electricity', 'meter', 'wifi', 'broadband', 'consumer', 'reading', 'gas', 'water', 'postpaid', 'prepaid'],
#     'grocery': ['bigbasket', 'milk', 'atta', 'sugar', 'sunflower oil', 'bread', 'vegetable', 'fruit', 'salt', 'paneer', 'brinjal', 'tomato', 'potato'],
#     'investment': ['endowment', 'grant', 'loan', 'applicant', 'income', 'expenditure', 'profit', 'interest', 'expense', 'finance', 'property', 'money', 'fixed deposit', 'kissan', 'vikas'],
#     'transport': ['car', 'cab', 'ola', 'uber', 'autorickshaw', 'railway', 'air', 'emirates', 'aerofloat', 'taxi', 'booking', 'road', 'highway'],
#     'shopping': ['dress', 'iphone', 'laptop', 'saree', 'max', 'pantaloons', 'westside', 'vedic', 'makeup', 'lipstick', 'cosmetics', 'mac', 'facewash', 'heels', 'crocs', 'footwear', 'purse', 'hair', 'ribbons'],
#     'education': ['pencil', 'pen', 'geometry box', 'ink', 'pages', 'book', 'books', 'notebook', 'textbook'],
#     'healthcare': ['medicine', 'hospital', 'doctor', 'pharmacy', 'medical', 'consultation', 'insurance', 'dentist', 'vaccination', 'surgery', 'treatment'],
#     'utilities': ['cable', 'subscription', 'Netflix', 'Amazon Prime', 'Hulu', 'Spotify', 'electricity bill', 'water bill', 'gas bill', 'internet bill'],
#     'personal_care': ['shampoo', 'conditioner', 'soap', 'lotion', 'deodorant', 'toothpaste', 'razor', 'skincare', 'haircare', 'fragrance', 'cosmetics'],
#     'dining_out': ['fast food', 'restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'sushi', 'fine dining', 'bar', 'pub', 'cocktail', 'dessert'],
#     'travel': ['flight', 'hotel', 'rental car', 'train', 'bus', 'taxi', 'fuel', 'toll', 'parking', 'luggage', 'passport', 'visa', 'travel insurance'],
#     'clothing': ['shirt', 'jeans', 'dress', 'shoes', 'accessories', 'underwear', 'socks', 'jacket', 'coat', 'hat', 'scarf', 'gloves', 'activewear'],
#     'electronics': ['smartphone', 'laptop', 'tablet', 'TV', 'camera', 'headphones', 'speakers', 'charger', 'cables', 'smartwatch', 'gaming console'],
#     'home_improvement': ['furniture', 'appliances', 'paint', 'tools', 'hardware', 'decor', 'lighting', 'flooring', 'renovation', 'landscaping', 'gardening'],
#     'subscriptions': ['magazine', 'newspaper', 'streaming service', 'gym membership', 'software', 'cloud storage', 'meal kit', 'wine club', 'beauty box'],
#     'gifts': ['birthday', 'anniversary', 'wedding', 'baby shower', 'holiday', 'Christmas', "Valentine's Day", "Mother's Day", "Father's Day", 'graduation'],
#     'pet_care': ['food', 'treats', 'toys', 'grooming', 'vet', 'medication', 'boarding', 'pet insurance', 'litter', 'leash', 'collar', 'bed'],
#     'car_maintenance': ['gas', 'oil change', 'car wash', 'tire rotation', 'repairs', 'maintenance', 'registration', 'insurance', 'parking fees', 'tolls'],
#     'kids': ['diapers', 'formula', 'baby food', 'clothing', 'toys', 'books', 'school supplies', 'activities', 'daycare', 'education expenses'],
#     'entertainment_outdoor': ['tickets', 'festivals', 'concerts', 'amusement parks', 'zoos', 'museums', 'sporting events', 'camping', 'hiking', 'picnics'],
#     'hobbies': ['crafting supplies', 'art supplies', 'musical instruments', 'lessons', 'classes', 'hobby-related equipment', 'materials'],
#     'taxes': ['income tax', 'property tax', 'sales tax', 'excise tax', 'vehicle tax', 'business tax', 'tax preparation fees', 'accountant fees'],
#     'insurance': ['health insurance', 'life insurance', 'car insurance', 'home insurance', 'renters insurance', 'travel insurance', 'pet insurance'],
#     'bank_fees': ['ATM fees', 'overdraft fees', 'wire transfer fees', 'foreign transaction fees', 'account maintenance fees', 'late payment fees'],
#     'utilities_home': ['garbage collection', 'sewage', 'recycling', 'pest control', 'maintenance fees', 'home security', 'alarm system'],
#     'personal_development': ['courses', 'workshops', 'seminars', 'coaching', 'self-help books', 'meditation apps', 'therapy', 'retreats'],
#     'charity': ['donations', 'fundraising events', 'sponsorships', 'volunteer expenses', 'charitable gifts', 'NGO contributions'],
#     'financial_services': ['financial advisor fees', 'investment management fees', 'brokerage fees', 'banking fees', 'loan interest'],
#     'sports': ['gym membership', 'equipment', 'apparel', 'team fees', 'event tickets', 'classes', 'coaching', 'sports gear maintenance'],
#     'beauty_services': ['salon', 'spa', 'haircut', 'coloring', 'manicure', 'pedicure', 'waxing', 'facials', 'massages', 'beauty treatments'],
#     'office_supplies': ['paper', 'pens', 'printer ink', 'envelopes', 'stamps', 'folders', 'binders', 'tape', 'staples', 'desk accessories'],
#     'repairs_maintenance': ['home repairs', 'appliance repairs', 'car repairs', 'maintenance services', 'handyman services'],
#     'home_cleaning': ['cleaning supplies', 'maid service', 'vacuum cleaner', 'mop', 'broom', 'cleaning solutions', 'laundry detergent'],
#     'eating_in': ['groceries', 'meal ingredients', 'cooking supplies', 'meal prep services', 'delivery fees', 'kitchenware'],
#     'entertainment_indoor': ['board games', 'puzzles', 'video games', 'streaming services', 'movie rentals', 'home theater equipment'],
#     'health_wellness': ['gym membership', 'fitness classes', 'yoga classes', 'meditation apps', 'supplements', 'wellness retreats'],
#     'travel_local': ['gas', 'public transportation', 'parking fees', 'tolls', 'day trips', 'local attractions', 'guided tours'],
#     'gardening': ['seeds', 'plants', 'tools', 'fertilizer', 'soil', 'pots', 'watering cans', 'gardening gloves', 'outdoor decor'],
#     'DIY_projects': ['materials', 'tools', 'equipment rental', 'project guides', 'DIY workshops', 'instructional books'],
#     'financial_planning': ['financial advisor fees', 'retirement planning services', 'investment advice', 'financial software'],
#     'home_decor': ['furniture', 'decor items', 'artwork', 'rugs', 'curtains', 'bedding', 'pillows', 'throws', 'candles'],
#     'home_security': ['alarm system', 'surveillance cameras', 'security service fees', 'locks', 'motion sensors'],
#     'photography': ['camera equipment', 'lenses', 'memory cards', 'photo editing software', 'prints', 'frames'],
#     'home_office': ['desk', 'chair', 'computer', 'printer', 'office supplies', 'organization tools', 'ergonomic accessories'],
#     'home_renovation': ['materials', 'contractor fees', 'permits', 'demolition', 'construction', 'remodeling'],
#     'self_care': ['spa treatments', 'massage therapy', 'meditation apps', 'yoga classes', 'wellness retreats'],
#     'financial_education': ['books', 'courses', 'seminars', 'workshops', 'online tutorials', 'educational subscriptions'],
#     'home_entertainment': ['streaming services', 'DVDs', 'Blu-rays', 'video games', 'board games', 'puzzles', 'home theater equipment'],
#     'socializing': ['dining out', 'drinks', 'events', 'parties', 'concerts', 'movies', 'sports games', 'activities']
# }


#     # Categorize bill based on keywords
#     for category, keywords in categories.items():
#         if any(word in tokens for word in keywords):
#             return category
#     return None


import joblib

svm_model = joblib.load('svm_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

@login_required
def billamount(request):
    if request.method == 'POST' and request.FILES['image']:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            text = extract_text_from_image(image)
            print(text)
            highest_amount = extract_highest_amount(text)
            
            category_name = predict_category(text)
            print("Highest Amount:", highest_amount)
            print("Category:", category_name)

            category, _ = Category.objects.get_or_create(name=category_name)

            if highest_amount and category:
                expense = Expense.objects.create(
                    user=request.user,
                    amount=highest_amount,
                    category=category,
                    content=f"Expense for {category_name}"
                )
                expense.save()
            return redirect('expense_statistics')

    else:
        form = ImageUploadForm()
    return render(request, 'upload_receipt.html', {'form': form})


def extract_text_from_image(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text


def extract_highest_amount(text):
    lines = [line for line in text.split('\n') if not re.search(r'\b\d{2}\.\d{2}\.\d{4}\b|\bBill\s+No\.\s*\d+\b', line)]

    amounts = []
    for line in lines:
        nums = re.findall(r'\b\d+(?:\.\d+)?\b', line)
        amounts.extend(map(float, nums))

    if amounts:
        return max(amounts)
    else:
        return None


def predict_category(text):
    text_tfidf = tfidf_vectorizer.transform([text])
    predicted_category = svm_model.predict(text_tfidf)[0]
    return predicted_category





# Expense report
import pandas as pd
from django.http import HttpResponse

def download_expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    
    # Create a DataFrame with the expense data
    expense_data = []
    for expense in expenses:
        expense_data.append({
            # 'Date': expense.date,
            'Amount': expense.amount,
            'Category': expense.category.name,
            'Content': expense.content
        })
    df = pd.DataFrame(expense_data)

    # Create an Excel writer object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="expenses.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response


# Income

from .forms import IncomeForm
from .models import Income

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('expense_statistics')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})