# Generated by Django 3.1.2 on 2020-11-03 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms', '0003_dedicatedhosts_os'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualhosts',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP'),
        ),
    ]
