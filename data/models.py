import hashlib, os
from datetime import datetime
from django.conf import settings
from django.db import models, connection

from users.models import CustomUser ,CustomUserProfile


class SpareClass(models.Model):
	name = models.CharField(max_length=100, unique=True)

class EquipmentClass(models.Model):
	name = models.CharField(max_length=100)
	spare_class = models.CharField(max_length=100)

class Denomination(models.Model):
	name = models.CharField(max_length=50, unique=True)

class Authority(models.Model):
	name = models.CharField(max_length=100, unique=True)

class Spares(models.Model):
	spare_class = models.CharField(max_length=100, default='')
	equipment_class = models.CharField(max_length=100, default='')
	pattern_number = models.SlugField(max_length=100, default='', blank=True)
	description = models.CharField(max_length=500, default='')	
	category_choices = [
		('PERMANENT', 'PERMANENT'),
		('RETURNABLE', 'RETURNABLE'),
		('CONSUMABLE', 'CONSUMABLE'),
	]
	category = models.CharField(max_length=20, default='PERMANENT', choices=category_choices)
	critical = models.BooleanField(default=False, blank=True)
	
	# Location specific details to be stored in the database
	compartment = models.CharField(max_length=200, default='UNKNOWN', blank=True)
	location = models.CharField(max_length=200, default='UNKNOWN', blank=True)
	# Quantity specific details
	denomination = models.CharField(max_length=20, default='')
	quantity_authorised = models.PositiveSmallIntegerField(default=0, blank=True)
	quantity_available = models.PositiveSmallIntegerField(default=0, blank=True)

	# Extra details regarding the spare
	authority = models.CharField(max_length=100, default='D787J')
	page = models.SlugField(max_length=100, default='', blank=True)
	line = models.PositiveSmallIntegerField(null=True, blank=True)
	remarks = models.CharField(max_length=200, null = True,blank=True, default='')

	# Image path as received from excel sheet
	def image_path(self, filename):
		name, extension = os.path.splitext(filename)
		if (extension in ['.png', '.jpg', '.jpeg']):
			# Check if the directory structure exists
			dir_spare_class = os.path.join(settings.MEDIA_ROOT, self.spare_class)
			dir_equipment_class = os.path.join(dir_spare_class, self.equipment_class)
			if (not os.path.isdir(dir_spare_class)):
				os.mkdir(dir_spare_class)
			if (not os.path.isdir(dir_equipment_class)):
				os.mkdir(dir_equipment_class)
			# Get the hash of the file
			file = self.image.open()
			data = file.read()
			filehash = hashlib.md5(data)
			return f'{self.spare_class}/{self.equipment_class}/{filehash.hexdigest()}{extension}'
		else:
			return f'default.png'

	# Image of the spare
	image = models.ImageField(upload_to=image_path, default=None, null=True, blank=True, max_length=500)


class Issue(models.Model):
	# The issued spare
	spare = models.ForeignKey(Spares, on_delete=models.PROTECT)
	# User to which the item is issued
	username = models.CharField(max_length=50, default='')
	quantity_issued = models.PositiveSmallIntegerField(default=0)
	issue_time = models.DateTimeField(auto_now_add=True, null=True)
	remarks = models.CharField(max_length=200, default='')

class IssueList(models.Model):     #temperory
	issue_entry = models.ForeignKey(Issue, on_delete=models.PROTECT)	
	quantity_toreturn = models.PositiveSmallIntegerField(default=0)
	
	
class Return(models.Model):
	# The issued spare
	spare = models.ForeignKey(Spares, on_delete=models.PROTECT)
	# User to which the item is issued
	username = models.CharField(max_length=50, default='')
	quantity_returned = models.PositiveSmallIntegerField(default=0)
	return_time = models.DateTimeField(auto_now_add=True, null=True)
	remarks = models.CharField(max_length=200, blank=True, default='')

class Survey(models.Model):  #temperory
	spare = models.ForeignKey(Spares, on_delete=models.PROTECT)
	quantity_tosurvey = models.PositiveSmallIntegerField(default=0)

class PostSurvey(models.Model):
	spare = models.ForeignKey(Spares, on_delete=models.PROTECT)
	quantity_surveyed = models.PositiveSmallIntegerField(default=0)
	survey_number = models.SlugField(max_length=50, default='NA')
	survey_number_date = models.DateTimeField(null=True)
	survey_report_date = models.DateTimeField(null=True)
	remarks = models.CharField(max_length=200, blank=True, default='')


class Demand(models.Model):   #temperory
	spare = models.ForeignKey(Spares, on_delete=models.PROTECT)
	quantity_todemand = models.PositiveSmallIntegerField(default=0)
	survey_entry = models.ForeignKey(PostSurvey, on_delete=models.PROTECT, null = True)	


class PostDemand(models.Model):
	spare = models.ForeignKey(Spares, on_delete=models.PROTECT)
	quantity_demanded = models.PositiveSmallIntegerField(default=0)
	demand_number = models.SlugField(max_length=50, default='')
	demand_date = models.DateTimeField(null=True)
	remarks = models.CharField(max_length=200, blank=True, default='')


class Receive(models.Model):    #temperory
	spare = models.ForeignKey(Spares, on_delete=models.PROTECT)
	quantity_toreceive = models.PositiveSmallIntegerField(default=0)
	demand_entry = models.ForeignKey(PostDemand, on_delete=models.PROTECT, null = True)
	

class PostReceive(models.Model):
	spare = models.ForeignKey(Spares, on_delete=models.PROTECT)
	quantity_received = models.PositiveSmallIntegerField(default=0)
	receipt_number = models.SlugField(max_length=50, default='')
	receive_date = models.DateTimeField(null=True)
	# authority = models.CharField(max_length=100, default='')
	remarks = models.CharField(max_length=200, blank=True, default='')

