# Generated by Django 5.0 on 2024-03-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0005_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['email']},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]