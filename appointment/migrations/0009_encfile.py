# Generated by Django 3.0.7 on 2021-06-28 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointment', '0008_payment_payment_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now=True, null=True)),
                ('file', models.FileField(upload_to='files')),
                ('from_user', models.CharField(max_length=200, null=True)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
