# Generated by Django 3.0.3 on 2020-09-05 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100, null=True)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('status', models.CharField(choices=[('In Stock', 'In Stock'), ('Unavailable', 'Unavailable')], max_length=20)),
                ('details', models.CharField(max_length=1000, null=True)),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]
