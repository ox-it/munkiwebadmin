from django.db import models
from django.conf import settings

from django.contrib.auth.models import User, Group
from reports.models import BusinessUnit

from manifests.models import Manifest

from datetime import datetime, timedelta

from jssmanifests.jsshelper import fetch_account_sites
from guardian.shortcuts import assign_perm

import jss
from string import atoi

# Create your models here.

try:
    BUSINESS_UNITS_ENABLED = settings.BUSINESS_UNITS_ENABLED
except:
    BUSINESS_UNITS_ENABLED = False

try:
    JSS_MAIN_SITE_NAME = settings.JSS_MAIN_SITE_NAME
except AttributeError:
    JSS_MAIN_SITE_NAME = 'Full Site Access'


## Helper functions
# This should live in jsshelpers, but this brings with it a cicular dependancy
# So ...

def sync_sites():

    # Sync time
    # This is a little icky 
    if JSSSite.objects.count() > 0:
        sync_obj = JSSSite.objects.earliest('last_refresh')
        try:
            site_cache = timedelta(seconds=settings.JSS_SITE_CACHE_TIME)
        except AttributeError:
            site_cache = timedelta(seconds=300)

        # Check freshness
        now   = datetime.now()
        delta =  now - sync_obj.last_refresh
        if delta < site_cache:
            return

    jss_connection = jss.JSS(user=settings.JSS_READONLY_USER,
                             password=settings.JSS_READONLY_PASS,
                             url=settings.JSS_URL,
                             ssl_verify=settings.JSS_VERIFY_CERT)

    jss_sites = jss_connection.Site()
    jss_site_dict = {}
    for jss_site in jss_sites:
        jss_site_dict[ jss_site['id'] ] = jss_site

        local_sites = JSSSite.objects.filter(jsssiteid__exact=jss_site['id'])
        if local_sites.count() > 1:
            # If there is more than one matching id, throw *all*
            # away, and start again
            local_sites.delete() ## XXX this needs testing

        if local_sites.count() == 1:
            site = local_sites[0]
            if site.jsssitename != jss_site['name']:
                site.jsssitename = jss_site['name']
                site.save()
                  
                site.businessunit.name = site.jsssitename
                site.businessunit.save()
        else:
            group, created = Group.objects.get_or_create( 
                name = 'JSS Site Access: %s' % jss_site['name'] )

            if BUSINESS_UNITS_ENABLED:
                bu, created   = BusinessUnit.objects.get_or_create( name = jss_site['name'] )
                site = JSSSite(jsssiteid   = jss_site['id'],
                               jsssitename = jss_site['name'],
                               businessunit = bu,
                               group = group )
            else: 
                site = JSSSite(jsssiteid   = jss_site['id'],
                               jsssitename = jss_site['name'],
                               group = group )
            site.save()
            assign_perm('can_view_jsssite', group, site)

    seen_full_site = False
    for local_site in JSSSite.objects.all():
            
        # Try not to remove the full site, hey ?
        if local_site.jsssiteid < 0 and seen_full_site:
            raise ValueError('Can only have one full site (i.e. with a negative jsssiteid)')
        elif local_site.jsssiteid < 0:
            seen_full_site = True
            local_site.jsssitename = settings.JSS_MAIN_SITE_NAME
            if BUSINESS_UNITS_ENABLED:
                bu, created = BusinessUnit.objects.get_or_create( 
                    name = JSS_MAIN_SITE_NAME )
                local_site.businessunit = bu
            local_site.save()
            continue

        local_site_id = '%d' % local_site.jsssiteid

        if not jss_site_dict.has_key( local_site_id ): 
            # Should we also delete the business unit and group ?
            # (Not sure; currently not, as this seems safest, but it may 
            # not be what people want/expect; perhaps this should be an
            # option in the future)
            local_site.delete()

    if not seen_full_site:
        group, created = Group.objects.get_or_create(
            name = 'JSS Site Access: %s' % settings.JSS_MAIN_SITE_NAME )

        if BUSINESS_UNITS_ENABLED:
            bu, created = BusinessUnit.objects.get_or_create( 
                name = settings.JSS_MAIN_SITE_NAME )
            site  = JSSSite(jsssiteid = -1,
                            jsssitename = settings.JSS_MAIN_SITE_NAME,
                            businessunit = bu, 
                            group = group )
        else:
            site  = JSSSite(jsssiteid = -1,
                            jsssitename = settings.JSS_MAIN_SITE_NAME,
                            group = group )

        site.save()
        assign_perm('can_view_jsssite', group, site)

    return


class JSSSite(models.Model):
    jsssiteid    = models.IntegerField('JSS Site ID')
    jsssitename  = models.CharField('Type Label', max_length=1024)
     # Um ... this might be currently pointless
    last_refresh = models.DateTimeField(auto_now=True)
    # /Um

    # 
    # Allow business units to be used, if enabled (and cope if not)
    # 
    businessunit = models.ForeignKey(BusinessUnit, null=True,
                                     blank=True, default=None,
                                     verbose_name = 'Business Unit' )

    # We are using groups to model permissions, so make sure each
    # site has a group
    group        = models.OneToOneField(Group, verbose_name = 'Related Group')

    class Meta:
       permissions = (
           ('can_view_jsssite', 'Can view JSS Site'),
           ('can_edit_jsssite', 'Can edit JSS Site'),
       )
       verbose_name        = 'JSS Site'
       verbose_name_plural = 'JSS Sites'

    def __unicode__(self):
        return '%s (JSS Site %d)' % (self.jsssitename, self.jsssiteid)


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
       verbose_name        = 'JSS Computer Attribute Type'
       verbose_name_plural = 'JSS Computer Attribute Types'

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
         models.ForeignKey(JSSComputerAttributeType,
                           verbose_name = 'Computer Attribute Type')

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

    priority  = models.IntegerField('Priority', default = 0)

    jsssite =  models.ForeignKey(JSSSite, verbose_name= 'JSS Site')

    # This is to let people temporarily enable and disable mappings
    enabled = models.BooleanField('Mapping enabled', default=True)

    class Meta:
       verbose_name        = 'JSS Computer Attribute Mapping'
       verbose_name_plural = 'JSS Computer Attribute Mappings'
       permissions = (
           ('can_view_jsscomputerattributemapping', 'Can view JSS Computer Attribute Mappings'),
       )

        

    def __unicode__(self):
        if self.jss_computer_attribute_type.xpath_needs_key: 
            return '%s: If %s matches %s then %s %s  (applies to site %s)' \
                % ( self.jss_computer_attribute_type.label, 
                    self.jss_computer_attribute_key,
                    self.jss_computer_attribute_value,
                    self.action(),
                    self.mapping_description(),
                    self.jsssite.jsssitename) 

        return '%s: If %s matches %s then %s %s (applies to site %s)' \
                % ( self.jss_computer_attribute_type.label, 
                    self.jss_computer_attribute_type.label,
                    self.jss_computer_attribute_value,
                    self.action(),
                    self.mapping_description(),
                    self.jsssite.jsssitename )


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

    def is_in_site(self,site_id):

        # Every mapping *should* have a site, but just to be sure:
        try:
            our_siteid = self.jsssite.jsssiteid
        except AttributeError: 
            return False # If no site set, we do not belong to it

        if our_siteid < 0:
            # i.e. the full JSS Site (which has id -1 in this app)
            return True 

        site_id = atoi(site_id) # Convert to int to be sure
        return (site_id == our_siteid)

    def computer_match(self,computer):
       
       # Check that we are in the correct site
       site_id = computer.findtext('general/site/id')
       if not self.is_in_site(site_id):
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


#
# A glue class for permissions modelling
#
class JSSUser(models.Model):

    user = models.OneToOneField(User)

    sites             = models.ManyToManyField(JSSSite,blank=True,
                                               verbose_name='JSS Site(s)')
    # We assume that user.name == JSS username, but looking up
    # information from the JSS (at least in version 9.72) via userid
    # gives a richer set of data
    # Sigh; one gets different information from calling account with 
    # name=%s and userid=%s
    # the former seems not to contain the 'Group access' string (even
    # when the user is setup for group access, but only 'Full Access'
    # or 'Site Access'
    # It also doesn't provide the group membership info
    jssuserid         = models.IntegerField('JSS User ID')
    last_site_refresh = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
       verbose_name        = 'JSS User'
       verbose_name_plural = 'JSS Users'

    def site_permissions(self):
       try:
           user_cache = timedelta(seconds=settings.JSS_USER_CACHE_TIME)
       except AttributeError:
           user_cache = timedelta(seconds=300)

       # Check freshness
       now   = datetime.now()
       delta =  now - self.last_site_refresh
       if delta < user_cache:
           return  

       # Step 0: Update sites with the JSS
       sync_sites()
       siteids = fetch_account_sites(self.user.username,self.jssuserid)
       # Step 1: Revoke membership of all *JSS* related groups
       # This could probably be more efficient (i.e look at
       # what needs to change and only change that)
       for group in self.user.groups.filter(jsssite__isnull=False):
          group.user_set.remove(self.user)
       for site in self.sites.all():
          self.sites.remove(site)

       # If the user has full site access, add them to all JSS Related groups
       if siteids == []:
           for group in Group.objects.filter(jsssite__isnull=False):
               group.user_set.add(self.user)
           for site in JSSSite.objects.all():
               self.sites.add(site)

       # If the user has some site access, add them to the right groups
       if siteids is not None:
           for sid in siteids:
               jsssite = JSSSite.objects.filter(jsssiteid=sid)[0]
               jsssite.group.user_set.add(self.user)
               self.sites.add(jsssite)
           # Add them to the full site too
           jsssite = JSSSite.objects.filter(jsssiteid__lt=0)[0]
           jsssite.group.user_set.add(self.user)
           self.sites.add(jsssite)
          
     
       # Update timestamp (as a marker 
       self.save()


