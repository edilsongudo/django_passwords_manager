# Generated by Django 4.0.6 on 2022-08-09 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passmanager', '0007_alter_masterpassword_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterpassword',
            name='salt',
            field=models.BinaryField(
                default=b'PLSE\xc7o\xder2\xb8>\xcf>}\x02\xf7]\\8\xfay\x1eM\xf4q\xd3G\xe4\xfa`\xf6 '
            ),
        ),
    ]