# Generated by Django 4.2 on 2023-05-02 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalaryInput', '0005_employee_classes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'ordering': ['CID', 'intrument', 'grade']},
        ),
        migrations.AddField(
            model_name='class',
            name='grade',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
