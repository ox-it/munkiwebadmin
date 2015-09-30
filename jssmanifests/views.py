from guardian.shortcuts import get_objects_for_user
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

from .models import JSSComputerAttributeMapping, JSSUser
from .decorators import jss_user_required

@login_required
@jss_user_required
def index(request):

    sites = get_objects_for_user(request.user, 'jssmanifests.can_view_jsssite')
    mappinglist = JSSComputerAttributeMapping.objects.filter(jsssite__exact=sites).\
      order_by('jss_computer_attribute_key','jss_computer_attribute_value','-priority')
    
    context = RequestContext(request, {'mapping_list': mappinglist})
    context.update(csrf(request))
    
    return render_to_response('jssmanifests/index.html', context)


@login_required
@permission_required('jssmanifests.can_change_jsscomputerattributemapping',
    login_url='/login/') 
def toggle_enabled(request, pk):

    mapping = JSSComputerAttributeMapping.objects.get(id=pk)
    mapping.enabled = not mapping.enabled
    mapping.save()

    return HttpResponseRedirect(reverse_lazy('index', current_app='jssmanifests'))



#@login_required
#@permission_required('jssmanifests.can_view_jssmanifests', login_url='/login/') 
class JSSComputerAttributeMappingDetail(DetailView):

    model = JSSComputerAttributeMapping


#@login_required
#@permission_required('jssmanifests.change_jssmanifests', login_url='/login/') 
class JSSComputerAttributeMappingUpdate(UpdateView):

    model = JSSComputerAttributeMapping
    fields = ['jss_computer_attribute_type','enabled','jsssite','priority']
    success_url = reverse_lazy('index', current_app='jssmanifests')


#@login_required
#@permission_required('jssmanifests.delete_jssmanifests', login_url='/login/') 
class JSSComputerAttributeMappingDelete(DeleteView):

    model = JSSComputerAttributeMapping
    success_url = reverse_lazy('index', current_app='jssmanifests')
    
    
