# Generated by Django 3.0 on 2022-01-08 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passmanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterpassword',
            name='salt',
            field=models.BinaryField(
                default=b'\xa8\xa4\x18\r\xdfJ\xca^\xcd\xbe\xad\xd5\xd1\x02\xeeJ\xfd\x9e+\x02&\xc5\x0b\x00\x9a\x8a(\x0fw\xab\x00;'
            ),
        ),
    ]
