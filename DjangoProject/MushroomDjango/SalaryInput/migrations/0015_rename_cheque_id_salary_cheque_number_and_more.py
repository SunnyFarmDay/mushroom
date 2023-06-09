# Generated by Django 4.2 on 2023-05-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalaryInput', '0014_salary_cheque_id_salary_created_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salary',
            old_name='cheque_id',
            new_name='cheque_number',
        ),
        migrations.AlterField(
            model_name='salary',
            name='created_time',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='paid_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
