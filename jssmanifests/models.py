from django.db import models

from manifests.models import Manifest

# Create your models here.

class JSSComputerAttributeType(models.Model):
    label = models.CharField('Type Label', max_length=1024)

    # This is is the XPath expression used to retrieve data from
    # a JSS computer recordData retrieved via a Computer JSS record
    # e.g //computer/general/site/name/text()
    computer_xpath = models.CharField('XPath expression', max_length=1024)

    # The following two variables are for use in order to give options
    # to a user. The idea is that we will query the the JSS using the 
    # api_path to get an XML result. The api_xpath then lets us extract
    # suitable values to present to the user to choose on a per-mapping basis
    api_path = models.CharField('API URI (api path to this object)',
                                max_length=1024,
                                blank=True)
    api_xpath = models.CharField(
        'API Xpath (expression to extract data from the API object)',
         max_length=1024,blank=True)

    # For some JSS items, we need a key to pick out the correct value(s) to
    # use - e.g. with an extension attribute we need to know the attribute 
    # name and then pull out the value for comparision. This flag says
    # whether or not a key is required; the default is that a key is not
    # required
    xpath_needs_key = models.BooleanField(
        'Key required for data extraction from xpath',
        default=False)

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

    jss_computer_attribute_type.short_description = 'Computer Attribute Type'

  
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

    # This is to let people temporarily enable and disable mappings
    enabled = models.BooleanField('Mapping enabled', default=True)

    class Meta:
       verbose_name        = 'Computer Attribute Mapping'
       verbose_name_plural = 'Computer Attribute Mappings'

    def __unicode__(self):
        if self.jss_computer_attribute_type.xpath_needs_key: 
            return '%s: If %s matches %s then %s %s ' \
                % ( self.jss_computer_attribute_type.label, 
                    self.jss_computer_attribute_key,
                    self.jss_computer_attribute_value,
                    self.action(),
                    self.mapping_description())

        return 'If %s matches %s then %s %s' \
                % ( self.jss_computer_attribute_type.label, 
                    self.jss_computer_attribute_value,
                    self.action(),
                    self.mapping_description())

    def action(self):
        if self.remove_from_xml:
            return 'remove'

        return 'add'

    def mapping_description(self):
        if self.manifest_element_type == 'c':
            type    = 'catalog'
            element = self.catalog_name

        if self.manifest_element_type == 'm':
            type    = 'manifest'
            element = self.manifest_name

        if self.manifest_element_type == 'p':
            type    = 'package'
            element = '%s to %s' % ( self.package_name, self.package_action)

        return '%s: %s' % (type, element)     

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
        if not self.enabled:
            return

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
