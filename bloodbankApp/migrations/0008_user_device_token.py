# Generated by Django 2.0.7 on 2018-07-25 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbankApp', '0007_bloodrequest_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='device_token',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]