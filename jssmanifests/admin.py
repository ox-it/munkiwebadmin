from django.contrib import admin

from django import forms

from manifests.models import Manifest

# Register your models here.

from jssmanifests.models import JSSComputerAttributeType, JSSComputerAttributeMapping


class JSSComputerAttributeTypeAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,               {'fields': ['label']}),
        ('Retrieval information', {'fields': ['xpath_expression',
                                              'api_endpoint'] }),
    ]

    def get_actions(self, request):
        actions = super(JSSComputerAttributeTypeAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
   
        return None


def _get_manifestlist():
    manifest_names = Manifest.list()
    return map(lambda x: (x,x), sorted( manifest_names ))

class JSSComputerAttributeMappingAdminForm(forms.ModelForm):

   class Meta:
        widgets = {
            'manifest_name': forms.widgets.Select( choices=_get_manifestlist() )
        }

class JSSComputerAttributeMappingAdmin(admin.ModelAdmin):

    #form = JSSComputerAttributeMappingAdminForm

    fieldsets = [
        (None,               {'fields': [ 'jss_computer_attribute_key',
                                          'jss_computer_attribute_value',
                                          'jss_computer_attribute_type',
                                          'manifest_element_type',
                                          'remove_from_xml',
                                          'priorty',
                                          'site',
            ]}),
        ('Catalog Settings', {'fields': [ 'catalog_name', ] } ),
        ('Manifest Settings', {'fields': ['manifest_name', ] } ),
        ('Package Settings', {'fields': ['package_name',
                                         'package_action'] }),
    ]

admin.site.register(JSSComputerAttributeType, JSSComputerAttributeTypeAdmin)
admin.site.register(JSSComputerAttributeMapping, JSSComputerAttributeMappingAdmin)
