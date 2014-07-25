from django.db import models

class Responses(models.Model):
	requests = models.ForeignKey("Requests", blank=True)
	responses = models.CharField(max_length=255, blank=True)


class Requests(models.Model):
	data_mode = models.CharField(max_length=255, blank=True)
	name = models.CharField(max_length=255, blank=True)
	method = models.CharField(max_length=255, blank=True)
	openi-object = models.ForeignKey("openi-object", blank=True)
	collection_id = models.CharField(max_length=255, blank=True)
	headers = models.CharField(max_length=255, blank=True)
	version = models.FloatField(blank=True)
	id_property = models.CharField(max_length=255, blank=True)
	timestamp = models.FloatField(blank=True)
	description = models.CharField(max_length=255, blank=True)
	url = models.CharField(max_length=255, blank=True)


class openiObject(models.Model):
	timestamp = models.FloatField(blank=True)
	name = models.CharField(max_length=255, blank=True)
	id_property = models.CharField(max_length=255, blank=True)


class Order(models.Model):
	openiObject = models.ForeignKey("openi-object", blank=True)
	order = models.CharField(max_length=255, blank=True)


class Data(models.Model):
	requests = models.ForeignKey("Requests", blank=True)
	data = models.CharField(max_length=255, blank=True)

