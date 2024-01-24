from collections import OrderedDict

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


def total_amount_spent():
    total_amount = Expense.objects.aggregate(sum=Sum('amount'))
    return total_amount['sum']

