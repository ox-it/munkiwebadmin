from django.db import models

# Create your models here.

class JSSComputerAttributeType(models.Model):
    label = models.CharField('Type Label', max_length=1024)
    xpath = models.CharField('XPath for extraction', max_length=1024,blank=True)
    api_endpoint = models.CharField('API Endpoint (data retrival)', max_length=1024,blank=True)

    class Meta:
       verbose_name        = 'Computer Attribute Type'
       verbose_name_plural = 'Computer Attribute Types'

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        print "HLLLLLLLL\n\n"
        super(JSSComputerAttributeType, self).save(*args, **kwargs)



