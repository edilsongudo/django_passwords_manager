# Generated by Django 3.0 on 2022-01-08 09:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterPassword',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'salt',
                    models.BinaryField(
                        default=b'\x15.\x7f\xe5`\xa0Hl\x9d\xf3\xce\xd0\rPZ\xe0E\xb9&\xe4P\xa8[\xd5\xe9e\xfa\xc7){\x13K'
                    ),
                ),
                (
                    'has_defined_a_master_password',
                    models.BooleanField(default=False),
                ),
                (
                    'author',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('site_name', models.CharField(default='', max_length=100)),
                (
                    'site_email_used',
                    models.EmailField(blank=True, default='', max_length=100),
                ),
                (
                    'site_password_used',
                    models.CharField(default='', max_length=100),
                ),
                (
                    'is_generated_for_initial_master_pw_check',
                    models.BooleanField(default=False),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
