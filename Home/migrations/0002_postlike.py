# Generated by Django 4.2.6 on 2023-10-13 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Accounts', '0005_alter_postcomment_replay'),
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_liked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_liked_related', to='Accounts.userpost')),
                ('user_liked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_liked_related', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
