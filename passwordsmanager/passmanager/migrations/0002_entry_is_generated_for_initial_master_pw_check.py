# Generated by Django 3.0 on 2022-01-02 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='is_generated_for_initial_master_pw_check',
            field=models.BooleanField(default=False),
        ),
    ]