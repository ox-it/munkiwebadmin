from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from django.conf import settings

# Create your views here.

from manifests.models import Manifest

import jss
import plistlib

def manifest(request, udid):

    if request.method == 'GET':

        # load base manifest from file system (either UDID or site_default)
        manifest = Manifest.read(udid)
        if not manifest:
            manifest = Manifest.read('site_default')

        jss_connection = jss.JSS(user=settings.JSS_READONLY_USER,
                                 password=settings.JSS_READONLY_PASS,
                                 url=settings.JSS_URL,
                                 ssl_verify=settings.JSS_VERIFY_CERT)

        computer = jss_connection.Computer('udid=%s' % udid.upper())
       
        if settings.JSSMANIFESTS_DEBUG_DUMPJSSEA:
            manifest['jss_extension_attributes']=[]
            for computer_ea in computer.iter('extension_attribute'):
                if computer_ea.find('value').text:
                    manifest['jss_extension_attributes'].append("%s = %s" % ( computer_ea.find('name').text, computer_ea.find('value').text))

        response = HttpResponse(content_type='application/xml')
        plistlib.writePlist(manifest, response)

        if settings.JSSMANIFESTS_DOWNLOAD_AS_ATTACHMENT:
            response['Content-Disposition'] = "attachment; filename=%s" % udid

    return response


