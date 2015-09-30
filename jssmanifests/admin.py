from django.conf import settings

from django.contrib import admin

from django import forms

import jss
import re
from django.http import HttpResponseRedirect

from manifests.models import Manifest
from catalogs.models import Catalog

from django.conf.urls import patterns,url

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import assign_perm

# Register your models here.

from jssmanifests.models import JSSComputerAttributeType, JSSComputerAttributeMapping,JSSSite,JSSUser,sync_sites

from reports.models import BusinessUnit

import jssmanifests.utils as utils

from django.contrib.auth.models import User, Group

try:
    BUSINESS_UNITS_ENABLED = settings.BUSINESS_UNITS_ENABLED
except AttributeError:
    BUSINESS_UNITS_ENABLED = False

try:
    JSS_MAIN_SITE_NAME = settings.JSS_MAIN_SITE_NAME
except AttributeError:
    JSS_MAIN_SITE_NAME = 'Full Site Access'

class JSSSiteAdminForm(forms.ModelForm):
 
    def __init__(self, *args, **kwargs):
        super(JSSSiteAdminForm, self).__init__(*args, **kwargs)

class JSSSiteAdmin(GuardedModelAdmin): # (admin.ModelAdmin):
   
    form = JSSSiteAdminForm
    actions = None

    def has_add_permission(self, request):
        return True

    # This (the add of the sync from the jss is icky
    def get_urls(self):
        urls = super(JSSSiteAdmin, self).get_urls()
        my_urls = [
            url(r'^sync/$', self.sync_jss),
        ]
        return my_urls + urls

    def sync_jss(self,request):
#        jss_connection = jss.JSS(user=settings.JSS_READONLY_USER,
#                                 password=settings.JSS_READONLY_PASS,
#                                 url=settings.JSS_URL,
#                                 ssl_verify=settings.JSS_VERIFY_CERT)
#
#        jss_sites = jss_connection.Site()
#        jss_site_dict = {}
#        for jss_site in jss_sites:
#            jss_site_dict[ jss_site['id'] ] = jss_site
#
#            local_sites = JSSSite.objects.filter(jsssiteid__exact=jss_site['id'])
#            if local_sites.count() > 1:
#                # If there is more than one matching id, throw *all*
#                # away, and start again
#                local_sites.delete() ## XXX this needs testing
#
#            if local_sites.count() == 1:
#                site = local_sites[0]
#                if site.jsssitename != jss_site['name']:
#                    site.jsssitename = jss_site['name']
#                    site.save()
#                  
#                    site.businessunit.name = site.jsssitename
#                    site.businessunit.save()
#            else:
#                group, created = Group.objects.get_or_create( jss_site['name'] )
#
#                if BUSINESS_UNITS_ENABLED:
#                    bu, created   = BusinessUnit.objects.get_or_create( name = jss_site['name'] )
#                    site = JSSSite(jsssiteid   = jss_site['id'],
#                                   jsssitename = jss_site['name'],
#                                   businessunit = bu,
#                                   group = group )
#                else: 
#                    site = JSSSite(jsssiteid   = jss_site['id'],
#                                   jsssitename = jss_site['name'],
#                                   group = group )
#                site.save()
#                assign_perm('can_view_jsssite', group, site)
#                bu.save()
#
#        seen_full_site = False
#        for local_site in JSSSite.objects.all():
#            
#           # Try not to remove the full site, hey ?
#           if local_site.jsssiteid < 0 and seen_full_site:
#               raise ValueError('Can only have one full site (i.e. with a negative jsssiteid)')
#           elif local_site.jsssiteid < 0:
#               seen_full_site = True
#               local_site.jsssitename      = JSS_MAIN_SITE_NAME
#               if BUSINESS_UNITS_ENABLED:
#                   local_site.businessunit.name = JSS_MAIN_SITE_NAME
#                   local_site.businessunit.save()
#               local_site.save()
#               continue
#
#           local_site_id = '%d' % local_site.jsssiteid
#
#           if not jss_site_dict.has_key( local_site_id ): 
#               # Should we also delete the business unit and group ?
#               # (Not sure; currently not, as this seems safest, but it may 
#               # not be what people want/expect; perhaps this should be an
#               # option in the future)
#               local_site.delete()
#
#        if not seen_full_site:
#            group, created = Group.objects.get_or_create( JSS_MAIN_SITE_NAME )
#            if BUSINESS_UNITS_ENABLED:
#                bu, created = BusinessUnit.objects.get_or_create( name = JSS_MAIN_SITE_NAME )
#                site  = JSSSite(jsssiteid = -1,
#                                jsssitename = JSS_MAIN_SITE_NAME,
#                                businessunit = bu, 
#                                group = group )
#            else:
#                site  = JSSSite(jsssiteid = -1,
#                                jsssitename = JSS_MAIN_SITE_NAME,
#                                group = group )
#
#            site.save()
#            assign_perm('can_view_jsssite', group, site)

        sync_sites()

        url = request.path
        redir = re.sub('sync/', '', url);
        return HttpResponseRedirect(redir) 


class JSSComputerAttributeTypeAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,               {'fields': ['label']}),
        ('Retrieval information', {'fields': ['computer_xpath',
                                              'api_path',
                                              'api_xpath',
                                              'xpath_needs_key' ] }),
    ]

    def get_actions(self, request):
        actions = super(JSSComputerAttributeTypeAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
   
        return None


class JSSComputerAttributeMappingAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JSSComputerAttributeMappingAdminForm, self).__init__(*args, **kwargs)
        manifest_name=self.instance.manifest_name
       # self.has_error(True)
       # self.add_error('manifest_name', 'FOO')
        choicelist, errors = utils.get_manifest_selectlist(manifest_name)

        self.fields['manifest_name'].widget = \
            forms.widgets.Select( choices=choicelist )
        self.fields['catalog_name'].widget  = \
            forms.widgets.Select( choices=utils.get_catalog_selectlist())
        self.fields['package_name'].widget  = \
            forms.widgets.Select( choices=utils.get_packagename_selectlist())

        self.is_valid()
        self.errors

    def clean_package_name(self):

        package_name = self.cleaned_data['package_name']
        package_name_list = utils.get_packagenamelist()

        if package_name and package_name_list.count(package_name) != 1:
            raise forms.ValidationError( "Package name %(pname)s is not in list of packages", params = { 'pname': package_name } ) 

        return package_name

    def clean_manifest_name(self):

        manifest_name = self.cleaned_data['manifest_name']
        manifest_list = utils.get_manifestlist()

        if manifest_name and manifest_list.count(manifest_name) != 1:
            raise forms.ValidationError( "Manifest name %(mname)s is not in list of manifests", params = { 'mname': manifest_name } ) 

        return manifest_name

    def clean_catalog_name(self):

        catalog_name = self.cleaned_data['catalog_name']
        catalog_list = utils.get_cataloglist()

        if catalog_name and catalog_list.count(catalog_name) != 1:
            raise forms.ValidationError( "Catalog name %(cname)s is not in list of catalogs", params = { 'cname': catalog_name } ) 

        return catalog_name


    def clean(self): 
      
        validation_errors = []

        cleaned_data = super(JSSComputerAttributeMappingAdminForm, self).clean()

        jss_computer_attribute_type = \
            cleaned_data.get('jss_computer_attribute_type')
        attribute_key =  cleaned_data.get('jss_computer_attribute_key')

        if jss_computer_attribute_type.xpath_needs_key and not attribute_key:
                validation_errors.append( forms.ValidationError( "Attribute type %(attribute_type)s requires a key for mapping", params = { 'attribute_type': jss_computer_attribute_type })  ) 

        if not jss_computer_attribute_type.xpath_needs_key and attribute_key:
                validation_errors.append( forms.ValidationError( "Attribute type %(attribute_type)s does not require a key for mapping", params = { 'attribute_type': jss_computer_attribute_type })  ) 

        # The following is long and ugly, but checks that the correct
        # set of fields is set for each mapping type
        manifest_element_type = cleaned_data.get('manifest_element_type')
        manifest_name         = cleaned_data.get('manifest_name')
        catalog_name          = cleaned_data.get('catalog_name')
        package_name          = cleaned_data.get('package_name')
        package_action        = cleaned_data.get('package_action')

        if manifest_element_type == 'c':
           if manifest_name:
                validation_errors.append( forms.ValidationError( "Catalog mappings should not have a manifest name set") ) 
 
           if not catalog_name:
                validation_errors.append( forms.ValidationError( "Catalog mappings should have a valid catalog name set") ) 

           if package_name:
               validation_errors.append( forms.ValidationError( "Catalog mappings should not have a package name set") ) 

           if package_action:
               validation_errors.append( forms.ValidationError( "Catalog mappings should not have a package action set") ) 

        if manifest_element_type == 'm':
           if not manifest_name:
                validation_errors.append( forms.ValidationError( "Manifest mappings should have a valid manifest name set") ) 
 
           if catalog_name:
                validation_errors.append( forms.ValidationError( "Manifest mappings should not have a catalog name set") ) 

           if package_name:
               validation_errors.append( forms.ValidationError( "Manifest mappings should not have a package name set") ) 

           if package_action:
               validation_errors.append( forms.ValidationError( "Manifest mappings should not have a package action set") ) 

        if manifest_element_type == 'p':
           if manifest_name:
                validation_errors.append( forms.ValidationError( "Package mappings should not have a manifest name set") ) 
 
           if catalog_name:
                validation_errors.append( forms.ValidationError( "Package mappings should not have a catalog name set") ) 

           print package_name
           if not package_name:
               validation_errors.append( forms.ValidationError( "Package mappings should have a valid package name set") ) 

           if not package_action:
               validation_errors.append( forms.ValidationError( "Package mappings should have a valid package action set") ) 

#        attribute_type = \
#            cleaned_data.get('jss_computer_attribute_type')

#        print self.instance
#
#        if xpath_needs_key \
#            and not cleaned_data.get('jss_computer_attribute_key'):
#            validation_errors.append( forms.ValidationError( "Mapping attribute type %(type)s needs a key, and there is not one set", params={'type': self.jss_computer_attribute_type.label} ) )
#
        # Look up relation and check xpath_needs_key
        # Check manifest given exists
#
        if len(validation_errors) > 0:
            raise forms.ValidationError(validation_errors)
       



class JSSComputerAttributeMappingAdmin(admin.ModelAdmin):

    form = JSSComputerAttributeMappingAdminForm

    fieldsets = [
        (None,               {'fields': [ 'jss_computer_attribute_key',
                                          'jss_computer_attribute_value',
                                          'jss_computer_attribute_type',
                                          'manifest_element_type',
                                          'remove_from_xml',
                                          'priority',
                                          'jsssite',
                                          'enabled',
            ]}),
        ('Catalog Settings', {'fields': [ 'catalog_name', ] } ),
        ('Manifest Settings', {'fields': ['manifest_name', ] } ),
        ('Package Settings', {'fields': ['package_name',
                                         'package_action'] }),
    ]

    list_display = ('__str__', 'enabled')

#   Bulk actions
#   Enable selected mappings
    def bulk_enable_attribute_mappings(self, request, queryset):
        self._bulk_enable_disable(request, queryset, True, 'enable')
    bulk_enable_attribute_mappings.short_description = "Enable selected mappings"
#   Disable selected mappings
    def bulk_disable_attribute_mappings(self, request, queryset):
        self._bulk_enable_disable(request, queryset, False, 'disable')

    bulk_disable_attribute_mappings.short_description = "Disable selected mappings"

    def _bulk_enable_disable(self, request, queryset, flag, action):
        rows_updated = queryset.update(enabled=flag)
        if rows_updated == 1:
            message_bit = "1 mapping was"
        else:
            message_bit = "%s mapping were" % rows_updated

        self.message_user(request, "%s successfully marked as %s." \
             % (message_bit, action) )


    actions = [ 'bulk_enable_attribute_mappings',
                'bulk_disable_attribute_mappings' ]

class JSSUserAdmin(admin.ModelAdmin):

    actions = None

    def has_add_permission(self, request):
        return True
 

admin.site.register(JSSUser, JSSUserAdmin)
admin.site.register(JSSSite, JSSSiteAdmin)
admin.site.register(JSSComputerAttributeType, JSSComputerAttributeTypeAdmin)
admin.site.register(JSSComputerAttributeMapping, JSSComputerAttributeMappingAdmin)
