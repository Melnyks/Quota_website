# Generated by Django 5.1.1 on 2024-10-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quota', '0003_registersubject'),
    ]

    operations = [
        migrations.AddField(
            model_name='registersubject',
            name='username',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
