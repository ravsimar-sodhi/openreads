# Generated by Django 2.2.3 on 2020-04-14 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_groupmember'),
    ]

    operations = [
        migrations.DeleteModel(
            name='groupMember',
        ),
    ]