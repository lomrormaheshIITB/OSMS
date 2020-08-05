from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.timezone import now
from .managers import CustomUserManager

class Department(models.Model):
	# populated by default using excel_todb.py
	name = models.CharField(max_length=50, unique=True)

class Rank(models.Model):
	# populated by default using excel_todb.py
	name = models.CharField(max_length=100,  unique=True)

class CustomUserProfile(models.Model):
	rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
	firstname = models.SlugField(max_length=50, default='')
	lastname = models.SlugField(max_length=50, blank=True, default='')	
	personal_number = models.SlugField(max_length=15, unique=True, default='')
	section = models.CharField(max_length=50, blank=True, default='')
	ship_joining_date = models.DateTimeField(default=now,null=True)
	ship_leaving_date = models.DateTimeField(null=True)
	remarks = models.CharField(max_length=200, default='')
	access_level_choices = [
		# first letter goes into the database , and second letter is for forms.py to show
		('0', 'ENGSUPERUSER'),
		('1','SUPERUSER'),   
		('2','STOREKEEPER'),
		('3','OTHERS')
	]
	access_level = models.CharField(max_length=20, default='2',null=True, choices=access_level_choices)
	department = models.ForeignKey(Department, on_delete=models.PROTECT)
	user_active = models.BooleanField(default=True)

class CustomUser(AbstractBaseUser):	
	username = models.CharField(max_length=100, unique=True)
	user_profile = models.ForeignKey(CustomUserProfile ,on_delete=models.PROTECT)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = CustomUserManager()	

	REQUIRED_FIELDS = ['user_profile']
	USERNAME_FIELD = 'username'

	def __str__(self):
		return self.username

	def has_perm(self, perm, object=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin
