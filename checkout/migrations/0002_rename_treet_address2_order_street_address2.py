# Generated by Django 5.1 on 2024-09-02 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='treet_address2',
            new_name='street_address2',
        ),
    ]
