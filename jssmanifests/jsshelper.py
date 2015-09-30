from django.conf import settings
import jss


def fetch_account_sites(username, jssuserid):

    jss_connection = jss.JSS( user = settings.JSS_READONLY_USER,
                              password = settings.JSS_READONLY_PASS,
                              url = settings.JSS_URL,
                              ssl_verify = settings.JSS_VERIFY_CERT)

    # Grab the account
    try:
       account = jss_connection.Account('userid=%s' % jssuserid)
    except jss.JSSGetError,  e:
       raise Exception('User %s not found (%s)' % (username, e))

    jssname = account.findtext('name')
    if jssname != username:
       raise Exception('User name (%s,%s) does not match for user id %s' % (jssname,username,jssuserid))
#
# Access is either: Full (everything + write (possibly) )
# Site (access to site + read only full site)
# Group (access to sites via groups + read only full site)
#
# CURRENTLY WE ASSUME READONLY ACCESS FOR EVERYTHING
#

    access_level = account.findtext('access_level')
    if access_level == 'Full Access':
        return []

    if access_level == 'Site Access':
        site = account.findtext('site/id')  
        return [ site, ]

    # Poo. The API doesn't seem to expose this
    if access_level == 'Group Access':
       return fetch_account_group_sites(jss_connection, account)

    return None

def fetch_account_group_sites(jss_connection, account):

    sites = None

    for group_element in account.findall('groups/group/id'):
        groupid = group_element.text
        jssgroup = jss_connection.AccountGroup('groupid=%s' % groupid)
        group_level = group.findtext('access_level')
        # If we have full access, just return, as we then don't need to
        # worry futher
        if  access_level == 'Full Access':
            return []

        if access_level == 'Site Access':
            site = group.findtext('site/id')  
            if sites is None:
                sites = []
                sites.append(site) 
          
    return sites

