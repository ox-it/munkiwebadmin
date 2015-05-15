from django.contrib import admin

from django import forms


# Register your models here.
from jssmanifests.models import JSSComputerAttributeType, JSSComputerAttributeMapping

class JSSComputerAttributeTypeAdminForm(forms.ModelForm):

    def clean(self): 
        cleaned_data = super(JSSComputerAttributeTypeAdminForm, self).clean()

        api_endpoint  = cleaned_data.get("api_endpoint")
        xpath = cleaned_data.get("xpath")

        if api_endpoint and xpath: 
            raise forms.ValidationError(
                'Cannot set both api endpoint and xpath',
                code='both api and xpath set')

        if not api_endpoint and not xpath:
            raise forms.ValidationError(
                'Must set one of api endpoint and xpath',
                code='neither api and xpath set')

class JSSComputerAttributeTypeAdmin(admin.ModelAdmin):

    form = JSSComputerAttributeTypeAdminForm

    fieldsets = [
        (None,               {'fields': ['label']}),
        ('Retrieval information', {'fields': ['xpath',
                                              'api_endpoint'] }),
    ]

    def get_actions(self, request):
        actions = super(JSSComputerAttributeTypeAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
   
        return None


class JSSComputerAttributeMappingAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,               {'fields': [ 'jss_computer_attribute_value',
                                          'jss_computer_attribute_type',
                                          'jss_computer_attribute_key',
                                          'manifest_element_type',
                                          'remove_from_xml',
                                          'priority',
                                          'site',
            ]}),
        ('Catalog Settings', {'fields': [ 'catalog_name', ] } ),
        ('Manifest Settings', {'fields': ['manifest_name', ] } ),
        ('Package Settings', {'fields': ['package_name',
                                         'package_action'] }),
    ]

admin.site.register(JSSComputerAttributeType, JSSComputerAttributeTypeAdmin)
admin.site.register(JSSComputerAttributeMapping, JSSComputerAttributeMappingAdmin)
