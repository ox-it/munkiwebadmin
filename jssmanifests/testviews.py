from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import RequestContext, loader
from guardian.shortcuts import get_objects_for_user
import jss
from lxml import etree
import re

from .models import JSSComputerAttributeMapping, JSSUser
from .decorators import jss_user_required
from manifests.models import Manifest


@login_required
@jss_user_required
def index(request):
     
    sites = get_objects_for_user(request.user, 'jssmanifests.can_view_jsssite')

    mappings = JSSComputerAttributeMapping.objects.filter(jsssite__exact=sites)

    template = loader.get_template('jssmanifests/index-test.html')
    context  = RequestContext(request, { 'mappings': mappings, 'sites': sites })

    return HttpResponse( template.render(context) )
