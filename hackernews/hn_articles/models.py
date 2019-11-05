from django.db import models

# Create your models here.

class Entries(models.Model):
	json_id =models.IntegerField()
	username = models.TextField()
	title = models.TextField()
	url = models.TextField()
	score = models.IntegerField()
	sentiment = models.TextField()
