from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from django.conf import settings

# Create your views here.

from manifests.models import Manifest

from jssmanifests.models import JSSComputerAttributeType

import jss
import plistlib

def manifest(request, manifest_name):

    if request.method == 'GET':

        # load base manifest from file system (either a specific one or site_default)
        manifest = Manifest.read(manifest_name)
        if not manifest:
            manifest = Manifest.read('site_default')

        jss_connection = jss.JSS(user=settings.JSS_READONLY_USER,
                                 password=settings.JSS_READONLY_PASS,
                                 url=settings.JSS_URL,
                                 ssl_verify=settings.JSS_VERIFY_CERT)

        computer = jss_connection.Computer('udid=%s' % manifest_name.upper())
       
        if settings.JSSMANIFESTS_DEBUG_DUMPJSSEA:
            _dump_computer_ea(manifest, computer.iter('extension_attribute') )

        attribute_types = JSSComputerAttributeType.objects.all()

        for type in attribute_types:
            if settings.JSSMANIFESTS_DEBUG_DUMPJSSEA:
                type.dump_debug_xml(manifest)
            choices = type.jsscomputerattributemapping_set.all()
            attributes = type.get_attributes(computer)

        response = HttpResponse(content_type='application/xml')
        plistlib.writePlist(manifest, response)

        if settings.JSSMANIFESTS_DOWNLOAD_AS_ATTACHMENT:
            response['Content-Disposition'] = "attachment; filename=%s" % udid

    return response

def _dump_list(tag, manifest, attr_list):

    manifest[tag] = []

    for attr in attr_list:
        name = attr.find('name').text
        val  = '(undef)'

        if attr.find('value').text:
            val = attr.find('value').text

        manifest[ tag ].append("%s = %s" % ( name, val) )

def _dump_computer_ea(manifest, attr_list):

    _dump_list('jss_extension_attributes', manifest, attr_list)

