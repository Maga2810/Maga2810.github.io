from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Partner(models. Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	alias = models.CharField(max_length=255, blank=False, editable=True)
	license = models.CharField(max_length=255, default=None)
	phone = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.user.username)

class Order(models. Model):
	title = models.CharField(max_length=255, blank=False, editable=True)
	category = models.CharField(max_length=255, blank=False, editable=True)
	quantity = models.IntegerField(default=0, blank=False, editable=True)
	year = models.CharField(max_length=255, blank=True, editable=True)
	brand = models.CharField(max_length=255, blank=True, editable=True)
	model = models.CharField(max_length=255, blank=True, editable=True)
	serial = models.CharField(max_length=255, blank=True, editable=True)
	link = models.CharField(max_length=600, blank=True, editable=True)
	location = models.CharField(max_length=255, blank=True, editable=True)
	notes = models.TextField(blank = True)
	partner = models.ForeignKey(Partner, related_name='orders')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "{2} Title {0} location {1}".format(self.title, self.location, self.created_at)