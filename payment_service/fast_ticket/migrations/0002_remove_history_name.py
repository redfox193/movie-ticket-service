# Generated by Django 5.0.3 on 2024-04-07 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fast_ticket', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='name',
        ),
    ]
