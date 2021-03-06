# Generated by Django 2.0.7 on 2018-07-25 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbankApp', '0004_auto_20180725_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.EmailField(max_length=254)),
                ('request_id', models.IntegerField()),
                ('user_response', models.BooleanField()),
                ('cab_needed', models.BooleanField()),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
