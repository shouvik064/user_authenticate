from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django import utils

# from common.models import *


# Create your models here.






class Admins(AbstractUser):
	""" auth user """

	status = [
		("0", "inactive"),
		("1", "active"),

	]
	# role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='role_admins',blank=True, null=True)
	company_id = models.CharField(max_length=200,null=True)
	firstname = models.CharField(max_length=200,null=False)
	lastname = models.CharField(max_length=200,null=False)
	address = models.TextField(null=False, blank=True)
	# country = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='admins_country',blank=True, null=True)
	# state = models.ForeignKey(States, on_delete=models.CASCADE, related_name='admins_state',blank=True, null=True)
	# city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='admins_city',blank=True, null=True)
	zip= models.CharField(default='',max_length=20, blank=True, null=True)
	phone = models.CharField(max_length=20, null=True, blank=True)
	last_login = models.DateTimeField(default=utils.timezone.now)
	last_login_ip = models.CharField(default='',max_length=20, blank=True, null=True)
	created = models.DateTimeField(default=utils.timezone.now, blank=True,null=True)
	modified = models.DateTimeField(default=utils.timezone.now, blank=True)
	last_activity = models.DateTimeField(default=utils.timezone.now)
	is_deleted = models.BooleanField(default=False)
	# es_deleted = models.BooleanField(default=False)
	status = models.CharField('Status', max_length=50,choices=status,default="1")
	defaultview = models.IntegerField(default=0,blank=True,null=True)
	# created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(null=True,default=utils.timezone.now)
	is_superuser = models.BooleanField(default=False,null=True)
	first_name = models.CharField(max_length=200,null=True)
	last_name = models.CharField(max_length=200,null=True)
	is_staff = models.BooleanField(default=False,null=True)
	is_active = models.BooleanField(default=False,null=True)
	date_joined = models.DateTimeField(default=utils.timezone.now, blank=True,null=True)

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'

	class Meta:
		db_table = 'admins'
		verbose_name = 'Admins'
		verbose_name_plural = 'Admins'

















class AdminColumnNames(models.Model):
	list_name = models.CharField(max_length=250)
	column_lists = models.TextField()
	createddate = models.DateTimeField(auto_now_add=True, null=True)
	updateddate = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		db_table = 'admin_column_names'

class UserPreferences(models.Model):
	user = models.ForeignKey(Admins, related_name="preference_of_user", on_delete=models.CASCADE,null=True)
	column_names = models.CharField(max_length=250)
	list_name = models.CharField(max_length=250)
	prefernces = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	updateddate= models.DateTimeField(default=utils.timezone.now, blank=True)

	class Meta:
		db_table = 'user_preferences'

class AdminLoginLogs(models.Model):

	admin = models.ForeignKey(Admins, related_name="admin_logs", on_delete=models.CASCADE,null=True)
	start_date_time = models.DateTimeField(blank=True,null=True)
	end_date_time = models.DateTimeField(blank=True,null=True)
	# isdeleted = models.BooleanField(default=False,db_column='deletedis')
	# es_deleted = models.BooleanField(default=False)


	class Meta:
		db_table = 'admin_login_logs'	
