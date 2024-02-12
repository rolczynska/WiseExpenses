import datetime
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'user',)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Expense(models.Model):
    class Meta:
        ordering = ('-date', '-pk')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    category = models.ForeignKey(Category, models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    date = models.DateField(default=datetime.date.today, db_index=True)

    def __str__(self):
        return f'{self.date} {self.name} {self.amount}'
