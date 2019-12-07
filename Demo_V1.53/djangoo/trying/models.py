# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DataSet(models.Model):
    field_id = models.IntegerField(db_column='_id', blank=True, null=False,primary_key=True)  # Field renamed because it started with '_'.
    report_num = models.IntegerField(db_column='REPORT_NUM', blank=True, null=True)  # Field name made lowercase.
    create_time = models.CharField(db_column='CREATE_TIME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    district_name = models.CharField(db_column='DISTRICT_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    district_id = models.IntegerField(db_column='DISTRICT_ID', blank=True, null=True)  # Field name made lowercase.
    street_name = models.CharField(db_column='STREET_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    street_id = models.IntegerField(db_column='STREET_ID', blank=True, null=True)  # Field name made lowercase.
    community_name = models.CharField(db_column='COMMUNITY_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    community_id = models.IntegerField(db_column='COMMUNITY_ID', blank=True, null=True)  # Field name made lowercase.
    event_type_name = models.CharField(db_column='EVENT_TYPE_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    event_type_id = models.IntegerField(db_column='EVENT_TYPE_ID', blank=True, null=True)  # Field name made lowercase.
    main_type_name = models.CharField(db_column='MAIN_TYPE_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    main_type_id = models.IntegerField(db_column='MAIN_TYPE_ID', blank=True, null=True)  # Field name made lowercase.
    sub_type_name = models.CharField(db_column='SUB_TYPE_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    sub_type_id = models.IntegerField(db_column='SUB_TYPE_ID', blank=True, null=True)  # Field name made lowercase.
    dispose_unit_name = models.CharField(db_column='DISPOSE_UNIT_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    dispose_unit_id = models.IntegerField(db_column='DISPOSE_UNIT_ID', blank=True, null=True)  # Field name made lowercase.
    event_src_name = models.CharField(db_column='EVENT_SRC_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    event_src_id = models.IntegerField(db_column='EVENT_SRC_ID', blank=True, null=True)  # Field name made lowercase.
    operate_num = models.IntegerField(db_column='OPERATE_NUM', blank=True, null=True)  # Field name made lowercase.
    overtime_archive_num = models.IntegerField(db_column='OVERTIME_ARCHIVE_NUM', blank=True, null=True)  # Field name made lowercase.
    intime_to_archive_num = models.IntegerField(db_column='INTIME_TO_ARCHIVE_NUM', blank=True, null=True)  # Field name made lowercase.
    intime_archive_num = models.IntegerField(db_column='INTIME_ARCHIVE_NUM', blank=True, null=True)  # Field name made lowercase.
    event_property_id = models.IntegerField(db_column='EVENT_PROPERTY_ID', blank=True, null=True)  # Field name made lowercase.
    event_property_name = models.CharField(db_column='EVENT_PROPERTY_NAME', blank=True, null=True, max_length=50)  # Field name made lowercase.
    occur_place = models.CharField(db_column='OCCUR_PLACE', blank=True, null=True, max_length=50)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'data_set'
    
    objects = models.Manager()

from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(db_column='USER_NAME', blank=True, null=True, max_length=50)
    unit_name = models.CharField(db_column='DISPOSE_UNIT_NAME', blank=True, null=True, max_length=50)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user.__str__()
    
    objects = models.Manager()
