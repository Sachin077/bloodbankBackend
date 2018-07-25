from django.db import models

# Create your models here.
class User(models.Model):
	GENDERS = (
		('M', 'Male'),
		('F', 'Female'),
	)
	emp_id = models.IntegerField(unique=True, null=True, blank=True)
	full_name = models.CharField(max_length=256)
	email_id = models.EmailField(unique=True)
	phone = models.BigIntegerField()
	gender = models.CharField(max_length=1, choices=GENDERS)
	blood_group = models.CharField(max_length=10)
	address = models.CharField(max_length=1024, null=True)
	city = models.CharField(max_length=100)
	fit_for_donation = models.BooleanField()
	password = models.CharField(max_length=256, default="PWD1234")
	device_token = models.CharField(max_length=1024, null=True, blank=True)

	def __unicode__(self):
		return str(self.email_id)

	def __str__(self):
		return str(self.email_id)

class BloodRequest(models.Model):
	STATUSES = (
		('Active', 'Active'),
		('Closed', 'Closed')
		)
	email_id = models.EmailField()
	blood_group = models.CharField(max_length=10)
	quantity = models.IntegerField()
	location = models.CharField(max_length=1024)
	city = models.CharField(max_length=100, default="Hyderabad")
	creationDate = models.DateTimeField()
	deadline = models.CharField(max_length=100)
	story = models.CharField(max_length=5000,null=True,blank=True)
	provideCab = models.BooleanField(default=False)
	status = models.CharField(max_length=10,choices=STATUSES,default="Active")
	feedback = models.CharField(max_length=1024,null=True,blank=True)

	def __unicode__(self):
		return str(self.email_id) + str(self.id)

	def __str__(self):
		return str(self.email_id) + str(self.id)

class Response(models.Model):
	email_id = models.EmailField()
	request_id = models.IntegerField()
	user_response = models.BooleanField()
	cab_needed = models.BooleanField()
	time = models.CharField(max_length=100)

	def __str__(self):
		return str(self.email_id) + " " + str(self.request_id)

