# Generated by Django 5.0.3 on 2024-03-14 09:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wild_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soumission',
            name='id_utilisateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]