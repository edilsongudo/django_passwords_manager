# Generated by Django 4.0.6 on 2022-08-09 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passmanager', '0005_alter_masterpassword_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterpassword',
            name='salt',
            field=models.BinaryField(
                default=b'\x86b\xcaK\x1b\xde\x14\\\xda\xd2\x8a\xc0\x14\x9d\x88z>\x0eU\xbb\xc5\\e{\x81\xef\xe8t\x17\x02\xc0j'
            ),
        ),
    ]