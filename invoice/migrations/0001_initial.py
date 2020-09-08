# Generated by Django 3.0.3 on 2020-09-08 05:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0005_orderitem_item_price'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('invoice_total', models.FloatField()),
                ('status', models.CharField(blank=True, choices=[('sent, sent', 'Sent'), ('paid', 'paid'), ('overdue', 'overdue'), ('created', 'created')], default='created', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_invoices', to='user.Customer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_invoices', to='order.Order')),
                ('sales_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_agent_invoices', to='user.SalesAgent')),
            ],
            options={
                'db_table': 'invoice',
            },
        ),
        migrations.CreateModel(
            name='FinancialLedger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('amount', models.FloatField()),
                ('balance', models.FloatField()),
                ('invoice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.Invoice')),
            ],
            options={
                'db_table': 'financial_ledger',
            },
        ),
    ]