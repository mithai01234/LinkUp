# Generated by Django 5.0 on 2024-03-02 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0008_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
