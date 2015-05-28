from django.db import models
from datetime import datetime
# Create your models here.

class ad_info(models.Model):
    ad_title = models.CharField(max_length=30)
    ad_coname = models.CharField(max_length=30)
    ad_cotype = models.CharField(max_length=30)
    ad_coindustry = models.CharField(max_length=30)
    ad_location = models.CharField(max_length=30)
    ad_yearcount = models.CharField(max_length=30)
    ad_degree = models.CharField(max_length=30)
    ad_treatment = models.CharField(max_length=30)
    ad_opinfo = models.CharField(max_length=1024)
    ad_coinfo = models.CharField(max_length=30)
    ad_cosize = models.CharField(max_length=30)
    ad_duty = models.CharField(max_length=30)
    ad_require = models.CharField(max_length=30)
    ad_custname = models.CharField(max_length=30)
    ad_phone = models.CharField(max_length=30)
    ad_email = models.CharField(max_length=30)
    ad_recruiting = models.CharField(max_length=30)
    ad_type = models.IntegerField(max_length=2)
    ad_imurl = models.CharField(max_length=1024)
    ad_links = models.CharField(max_length=1024)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField()

    def __unicode__(self):
        return u'adinfo-%s' % (self.id)

    class Admin:
        pass

class ad_status(models.Model):
    ad_id=models.ForeignKey(ad_info)
    ad_effective = models.DateField()
    ad_expiry = models.DateField()
    ad_status = models.IntegerField(max_length=2)
    ad_vistcount = models.IntegerField(max_length=30)
    createtime = models.DateTimeField()
    updatetime = models.DateTimeField()

    def __unicode__(self):
        return u'adstatus-%s' % (self.id)

    class Admin:
        pass

