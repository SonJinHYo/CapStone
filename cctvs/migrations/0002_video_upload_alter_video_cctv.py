# Generated by Django 4.1.7 on 2023-04-10 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cctvs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='upload',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='video',
            name='cctv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='cctvs.cctv', verbose_name='CCTV'),
        ),
    ]
