from functools import wraps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import jss

from .models import JSSUser


def _get_jss_user_id(username):

    jss_connection = jss.JSS(user=settings.JSS_READONLY_USER,
                             password=settings.JSS_READONLY_PASS,
                             url=settings.JSS_URL,
                             ssl_verify=settings.JSS_VERIFY_CERT)

    try:
       account = jss_connection.Account('name=%s' % username)
       userid = account.findtext('id')
    except jss.JSSGetError,  e:
       raise Exception('User %s not found (%s)' % (username, e))

    return userid


def jss_user_required(f):
    """ Decorator that sets up the user <-> jssuser mapping (and thus
        ensures that site permissions can go on """
    @wraps(f)
    def decorator(request, *args, **kwargs):
        user = request.user
        try:
            user.jssuser.site_permissions()
        except ObjectDoesNotExist:
            jid = _get_jss_user_id(user.username)
            juser = JSSUser(user=user, jssuserid=jid)
            juser.save()
            user.jssuser.site_permissions()
        return f(request, *args, **kwargs)

    return decorator
