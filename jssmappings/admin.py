from django.contrib import admin

from django import forms


# Register your models here.
from jssmappings.models import JSSComputerAttributeType


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

    def save(self, *args, **kwargs):
        super(JSSComputerAttributeType, self).save(*args, **kwargs) 

    def get_actions(self, request):
        actions = super(JSSComputerAttributeTypeAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
   
        return None



admin.site.register(JSSComputerAttributeType, JSSComputerAttributeTypeAdmin)
