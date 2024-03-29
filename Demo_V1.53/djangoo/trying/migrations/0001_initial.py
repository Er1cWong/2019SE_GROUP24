# Generated by Django 2.2.7 on 2019-11-18 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('field_id', models.IntegerField(blank=True, db_column='_id', primary_key=True, serialize=False)),
                ('report_num', models.IntegerField(blank=True, db_column='REPORT_NUM', null=True)),
                ('create_time', models.CharField(blank=True, db_column='CREATE_TIME', max_length=50, null=True)),
                ('district_name', models.CharField(blank=True, db_column='DISTRICT_NAME', max_length=50, null=True)),
                ('district_id', models.IntegerField(blank=True, db_column='DISTRICT_ID', null=True)),
                ('street_name', models.CharField(blank=True, db_column='STREET_NAME', max_length=50, null=True)),
                ('street_id', models.IntegerField(blank=True, db_column='STREET_ID', null=True)),
                ('community_name', models.CharField(blank=True, db_column='COMMUNITY_NAME', max_length=50, null=True)),
                ('community_id', models.IntegerField(blank=True, db_column='COMMUNITY_ID', null=True)),
                ('event_type_name', models.CharField(blank=True, db_column='EVENT_TYPE_NAME', max_length=50, null=True)),
                ('event_type_id', models.IntegerField(blank=True, db_column='EVENT_TYPE_ID', null=True)),
                ('main_type_name', models.CharField(blank=True, db_column='MAIN_TYPE_NAME', max_length=50, null=True)),
                ('main_type_id', models.IntegerField(blank=True, db_column='MAIN_TYPE_ID', null=True)),
                ('sub_type_name', models.CharField(blank=True, db_column='SUB_TYPE_NAME', max_length=50, null=True)),
                ('sub_type_id', models.IntegerField(blank=True, db_column='SUB_TYPE_ID', null=True)),
                ('dispose_unit_name', models.CharField(blank=True, db_column='DISPOSE_UNIT_NAME', max_length=50, null=True)),
                ('dispose_unit_id', models.IntegerField(blank=True, db_column='DISPOSE_UNIT_ID', null=True)),
                ('event_src_name', models.CharField(blank=True, db_column='EVENT_SRC_NAME', max_length=50, null=True)),
                ('event_src_id', models.IntegerField(blank=True, db_column='EVENT_SRC_ID', null=True)),
                ('operate_num', models.IntegerField(blank=True, db_column='OPERATE_NUM', null=True)),
                ('overtime_archive_num', models.IntegerField(blank=True, db_column='OVERTIME_ARCHIVE_NUM', null=True)),
                ('intime_to_archive_num', models.IntegerField(blank=True, db_column='INTIME_TO_ARCHIVE_NUM', null=True)),
                ('intime_archive_num', models.IntegerField(blank=True, db_column='INTIME_ARCHIVE_NUM', null=True)),
                ('event_property_id', models.IntegerField(blank=True, db_column='EVENT_PROPERTY_ID', null=True)),
                ('event_property_name', models.CharField(blank=True, db_column='EVENT_PROPERTY_NAME', max_length=50, null=True)),
                ('occur_place', models.CharField(blank=True, db_column='OCCUR_PLACE', max_length=50, null=True)),
            ],
            options={
                'db_table': 'data_set',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, db_column='USER_NAME', max_length=50, null=True)),
                ('unit_name', models.CharField(blank=True, db_column='DISPOSE_UNIT_NAME', max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
            },
        ),
    ]
