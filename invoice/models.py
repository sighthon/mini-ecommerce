from datetime import datetime

from django.db import models

from order.models import Order
from user.models import Customer, SalesAgent


class Invoice(models.Model):
    """Model for  Invoice"""

    class Meta:
        db_table = "invoice"

    class StatusChoices(models.TextChoices):
        SENT = "sent, sent"
        PAID = "paid", "paid"
        OVERDUE = "overdue", "overdue"
        CREATED = "created", "created"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, related_name="order_invoices")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, related_name="customer_invoices")
    sales_agent = models.ForeignKey(SalesAgent, on_delete=models.CASCADE, null=False,
                                    related_name="sales_agent_invoices")
    invoice_date = models.DateTimeField(default=datetime.utcnow, null=False)
    invoice_total = models.FloatField(null=False)
    status = models.CharField(null=False, blank=True, choices=StatusChoices.choices, max_length=20, default="created")


class FinancialLedger(models.Model):
    """Model for Financial Ledger"""

    class Meta:
        db_table = 'financial_ledger'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, related_name="order_ledgers")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False, related_name="customer_ledgers")
    transaction_date = models.DateTimeField(default=datetime.utcnow)
    amount = models.FloatField(null=False)
    balance = models.FloatField(null=False)


