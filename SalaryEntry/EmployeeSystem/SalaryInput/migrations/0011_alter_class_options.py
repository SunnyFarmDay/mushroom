# Generated by Django 4.2 on 2023-05-02 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SalaryInput', '0010_alter_class_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'ordering': ['type', 'duration', 'level']},
        ),
    ]
