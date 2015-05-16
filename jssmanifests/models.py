from django.db import models

# Create your models here.

class JSSComputerAttributeType(models.Model):
    label = models.CharField('Type Label', max_length=1024)

    # Data retrieved via a JSS record
    jss_field = models.CharField('JSS Field name', max_length=1024, blank=True)

    api_endpoint = models.CharField('API Endpoint (data retrival)', max_length=1024,blank=True)

    class Meta:
       verbose_name        = 'Computer Attribute Type'
       verbose_name_plural = 'Computer Attribute Types'

    def __unicode__(self):
        return self.label
 
    def get_attributes(self, computer):
       if self.jss_field:
           return self.jss_extract(computer)

       return None

    def jss_extract(self, computer):
        return None

    def dump_debug_xml(self,manifest):
       if not manifest.has_key('jss_attribute_types'): 
           manifest['jss_attribute_types']=[]
       if not manifest.has_key('jss_attribute_type_sets'): 
            manifest['jss_attribute_type_sets']={}

       choices = self.jsscomputerattributemapping_set.all()

       manifest['jss_attribute_types'].append("%s = %s choices" % 
                                  (self.label, choices.count() ) )  

       manifest['jss_attribute_type_sets'][self.label]=[]

       choices_list = manifest['jss_attribute_type_sets'][self.label]
       for ch in choices:
           choices_list.append('%s' % (ch,) )





class JSSComputerAttributeMapping(models.Model):

    MANIFEST_ELEMENTS = [
        ('c', 'Catalog'),
        ('m', 'Manifest'),
        ('p', 'Package'),
    ]

    PACKAGE_ACTIONS = [
        ('managed_installs', 'Managed installs'),
        ('managed_uninstalls', 'Managed uninstalls'),
        ('managed_updates', 'Managed updates'),
        ('optional_installs', 'Optional installs'),
    ]

    jss_computer_attribute_type = \
         models.ForeignKey(JSSComputerAttributeType) 
  
    jss_computer_attribute_key   = models.CharField('Attribute Key',
                                                    max_length=1024)
    jss_computer_attribute_value = models.CharField('Attribute Value',
                                                    max_length=1024)

    manifest_element_type        = models.CharField('Manifest Element',
                              choices=MANIFEST_ELEMENTS, max_length='1' )

    catalog_name   = models.CharField('Catalog Name', max_length=1024,
                                       blank=True)

    package_name   = models.CharField('Package Name', max_length=1024, blank=True)
    package_name   = models.CharField('Package Name', max_length=1024, blank=True)
    package_action = models.CharField('Package Action',
                        choices=PACKAGE_ACTIONS, blank=True, max_length=256)

    manifest_name   = models.CharField('Manifest Name', max_length=1024, blank=True)

    remove_from_xml   = models.BooleanField('Remove from Manifest')

    priority  = models.IntegerField('Priorty')

    site   = models.CharField('Site', max_length=1024, blank=True)

    class Meta:
       verbose_name        = 'Computer Attribute Mapping'
       verbose_name_plural = 'Computer Attribute Mappings'

    def __unicode__(self):
        return '%s: %s -> %s (%s)' % ( self.jss_computer_attribute_type.label, 
               self.jss_computer_attribute_key,
               self.jss_computer_attribute_value,
               self.manifest_element_type)
 
