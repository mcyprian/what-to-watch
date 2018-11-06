# Generated by Django 2.1.3 on 2018-11-06 20:46

from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('epg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=128, unique=True)),
                ('photo', stdimage.models.StdImageField(blank=True, upload_to='media/')),
            ],
        ),
        migrations.AlterField(
            model_name='actor',
            name='uid',
            field=models.BigIntegerField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='uid',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='epgentity',
            name='uid',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='title',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AddField(
            model_name='image',
            name='epg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epg.EPGEntity'),
        ),
    ]