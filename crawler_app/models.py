from django.db import models
# Create your models here.

class HtmlPages(models.Model) :
    link = models.CharField(max_length=200)
    linkdata = models.TextField()

class PdfPages(models.Model) :
    link = models.CharField(max_length=200)
    linkdata = models.TextField()

class ImageLinks(models.Model) :
    link = models.CharField(max_length=200)
