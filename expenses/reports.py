from datetime import datetime
import decimal
from collections import OrderedDict, defaultdict

from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from .models import Expense


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def total_amount_spent(queryset):
    total_amount = queryset.aggregate(total_amount=Sum('amount'))
    return total_amount['total_amount']


def summary_per_month(queryset):
    all_expenses = queryset.values('date', 'amount')

    summary = defaultdict(decimal.Decimal)

    for expense in all_expenses:
        year_month = datetime.strptime(str(expense['date']), '%Y-%m-%d').strftime('%Y-%m')
        summary[year_month] += decimal.Decimal(expense['amount'])

    return dict(summary)


def number_expenses_per_category():
    all_expenses = Expense.objects.values('category', 'amount')

    expenses_per_category = defaultdict(int)

    for expense in all_expenses:
        expenses_per_category[expense['category']] += 1

    return dict(expenses_per_category)
