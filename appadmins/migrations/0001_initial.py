# Generated by Django 3.2.6 on 2022-09-05 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('tag_name', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
