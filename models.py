from django.db import models

# Create your models here.
class EEG_DataM(models.Model):
    EFileId = models.AutoField(primary_key=True)
    EFileName = models.CharField(max_length=500)

class DemoM(models.Model):
    DFileId = models.AutoField(primary_key=True)
    DFileName = models.CharField(max_length=500)