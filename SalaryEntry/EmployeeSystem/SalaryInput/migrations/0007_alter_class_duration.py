# Generated by Django 4.2 on 2023-05-02 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalaryInput', '0006_alter_class_options_class_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='duration',
            field=models.CharField(max_length=3),
        ),
    ]
