# Generated by Django 5.1.3 on 2024-11-30 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urticket_app', '0005_member_user_organizer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, default='bg.jpeg', upload_to='event_images/'),
        ),
    ]