# Generated by Django 4.2 on 2023-05-02 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SalaryInput', '0007_alter_class_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'ordering': ['CID', 'instrument', 'grade']},
        ),
        migrations.RenameField(
            model_name='class',
            old_name='intrument',
            new_name='instrument',
        ),
    ]