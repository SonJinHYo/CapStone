# Generated by Django 4.1.7 on 2023-03-28 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CCTV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='모델명')),
                ('region', models.CharField(max_length=50, verbose_name='감시 지역')),
                ('description', models.TextField(blank=True, verbose_name='상세 주소 / 추가 설명')),
            ],
        ),
    ]
