from django.db import models

from manifests.models import Manifest

# Create your models here.

class JSSComputerAttributeType(models.Model):
    label = models.CharField('Type Label', max_length=1024)

    # Data retrieved via a JSS record
    computer_xpath = models.CharField('XPath expression', max_length=1024)

    api_path = models.CharField('API URI (api path to this object)', max_length=1024,blank=True)
    api_xpath = models.CharField('API Xpath (expression to extract data from the API object)', max_length=1024,blank=True)

    xpath_needs_key = models.BooleanField('Key required for data extraction', default=False)


    class Meta:
       verbose_name        = 'Computer Attribute Type'
       verbose_name_plural = 'Computer Attribute Types'

    def __unicode__(self):
        return self.label
 
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

    def get_data(self, computer, key):
        rv = computer.xpath(self.computer_xpath, key=key)
        return rv


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
                                                    max_length=1024, blank=True)
    jss_computer_attribute_value = models.CharField('Attribute Value',
                                                    max_length=1024)

    manifest_element_type        = models.CharField('Manifest Element',
                              choices=MANIFEST_ELEMENTS, max_length='1' )

    catalog_name   = models.CharField('Catalog Name', max_length=1024,
                                       blank=True)

    package_name   = models.CharField('Package Name',
                                          max_length=1024, blank=True)

    package_action = models.CharField('Package Action',
                        choices=PACKAGE_ACTIONS, blank=True, max_length=256)

    manifest_name   = models.CharField('Manifest Name', max_length=1024,
                                blank=True) 

    remove_from_xml   = models.BooleanField('Remove from Manifest')

    priorty  = models.IntegerField('Priorty', default = 0)

    site   = models.CharField('Site', max_length=1024, blank=True)

    class Meta:
       verbose_name        = 'Computer Attribute Mapping'
       verbose_name_plural = 'Computer Attribute Mappings'

    def __unicode__(self):
        return '%s: %s -> %s (%s)' % ( self.jss_computer_attribute_type.label, 
               self.jss_computer_attribute_key,
               self.jss_computer_attribute_value,
               self.manifest_element_type)

    def is_in_site(self,site):
        if not self.site or self.site == site:
            return True
        return False

    def computer_match(self,computer):
       
       # Check that we are in the correct site
       site = computer.findtext('general/site')
       if not self.is_in_site(site):
           return False 
       
       elements = self.jss_computer_attribute_type.get_data(computer,self.jss_computer_attribute_key);
       for value in elements:
           if value == self.jss_computer_attribute_value:
               return True
       
       return False

    def apply_mapping(self,manifest):
        if self.manifest_element_type == 'c':
            self.update_manifest_catalog(manifest)

        if self.manifest_element_type == 'm':
            self.update_manifest_manifest(manifest)

        if self.manifest_element_type == 'p':
            self.update_manifest_package(manifest)

        return

    # Question: should we always remove, then add (so that priorties have
    #           a real effect ?
    def _update_list(self, list, name):

       if self.remove_from_xml:
           while list.count(name) > 0:
               list.remove(name)
           return
  
       if list.count(name) <= 0:
           list.append(name)

       return 

    def update_manifest_catalog(self, manifest):
        if not manifest.has_key('catalogs'):
           manifest['catalogs'] = []

        self._update_list(manifest['catalogs'], self.catalog_name)

        return
  
    def update_manifest_manifest(self, manifest):
        if not manifest.has_key('included_manifests'):
           manifest['included_manifests'] = []

        self._update_list(manifest['included_manifests'], self.manifest_name)
        return 

    def update_manifest_package(self, manifest):
        if not manifest.has_key(self.package_action):
           manifest[self.package_action] = []

        self._update_list(manifest[self.package_action], self.package_name)
        return 
