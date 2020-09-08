from rest_framework import serializers

from .models import Invoice, FinancialLedger


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["order", "customer", "sales_agent", "invoice_total", "status"]


class FinancialLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialLedger
        fields = ["order", "customer", "amount", "balance", "customer"]
