# Generated by Django 5.1.1 on 2024-09-29 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_expense_frequency_expense_is_recurring_member_role_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='frequency',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='is_recurring',
        ),
        migrations.RemoveField(
            model_name='member',
            name='role',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]