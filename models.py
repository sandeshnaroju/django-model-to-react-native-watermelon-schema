import uuid

from django.db import models

from billing.models import Bill
from billing.models import Customer
from business.models import Business
from files.models import File
from inventory.models import Supplier, Inventory
from payments.models import Gateway


class Income(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, related_name='incomes', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True)
    description = models.TextField(blank=True)
    payment_method = models.ForeignKey(Gateway, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name) +  str(self.bill.number)


class IncomeAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    income = models.ForeignKey(Income, on_delete=models.CASCADE, related_name="incomeattachments")
    name = models.CharField(max_length=100, default="")
    url = models.ForeignKey(File, on_delete=models.CASCADE, related_name="income_attachment_url")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " " + str(self.created)


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, related_name='expenses', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True)
    description = models.TextField(blank=True)
    payment_method = models.ForeignKey(Gateway, on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class ExpenseAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="expenseattachments")
    name = models.CharField(max_length=100, default="")
    url = models.ForeignKey(File, on_delete=models.CASCADE, related_name="expense_attachment_url")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " " + str(self.created)
