# Generated by Django 4.0.6 on 2022-07-24 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passmanager', '0003_alter_masterpassword_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterpassword',
            name='salt',
            field=models.BinaryField(default=b'\x0ed\xf3Nr\xdc7\xccZ\x0f\xbd<\xe0\t\xb2\xa2\xaemy\x14>,\xcc.\\\xcep\xfa.\xb8;\x8b'),
        ),
    ]