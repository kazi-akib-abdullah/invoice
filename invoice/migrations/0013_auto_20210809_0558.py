# Generated by Django 3.0.8 on 2021-08-08 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0012_auto_20210809_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='message',
            field=models.TextField(blank=True, default='this is a default message.', null=True),
        ),
    ]
