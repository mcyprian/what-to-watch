# Generated by Django 2.1.3 on 2018-11-05 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Broadcasting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('starts_at', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.BigIntegerField()),
                ('title', models.CharField(max_length=128)),
                ('order', models.PositiveIntegerField(null=True)),
                ('channel_type', models.CharField(max_length=128, null=True)),
                ('television', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EPGEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.BigIntegerField()),
                ('title', models.CharField(max_length=128)),
                ('length', models.PositiveIntegerField(null=True)),
                ('summary', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('original_title', models.CharField(max_length=128, null=True)),
                ('year', models.PositiveIntegerField(null=True)),
                ('state', models.CharField(max_length=128, null=True)),
                ('channels', models.ManyToManyField(through='epg.Broadcasting', to='epg.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipatesIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=128)),
                ('role_name', models.CharField(max_length=128, null=True)),
                ('epg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epg.EPGEntity')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='epg.Person')),
                ('uid', models.BigIntegerField(null=True)),
            ],
            bases=('epg.person',),
        ),
        migrations.AddField(
            model_name='participatesin',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epg.Person'),
        ),
        migrations.AddField(
            model_name='epgentity',
            name='genres',
            field=models.ManyToManyField(to='epg.Genre'),
        ),
        migrations.AddField(
            model_name='epgentity',
            name='persones',
            field=models.ManyToManyField(through='epg.ParticipatesIn', to='epg.Person'),
        ),
        migrations.AddField(
            model_name='broadcasting',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epg.Channel'),
        ),
        migrations.AddField(
            model_name='broadcasting',
            name='epg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epg.EPGEntity'),
        ),
    ]
