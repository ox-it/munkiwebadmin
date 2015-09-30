from django.test import TestCase, override_settings
from django.test import Client
from django.conf import settings
from django.db.utils import IntegrityError

from lxml import etree


import os

from jssmanifests.models import JSSComputerAttributeType,JSSComputerAttributeMapping,JSSSite

from manifests.models import Manifest

# Create your tests here.
cwd = os.path.dirname(os.path.abspath(__file__))
test_repo_dir = 'example-data/repo/'

class JSSComputerAttributeTypeTest(TestCase):
   
   fixtures = [ 'mapping_types', ]

   def test_mapping_extension_attribute(self):
       types = JSSComputerAttributeType.objects.filter(label__exact='Extension Attribute')
       self.assertEqual(types.count(),1)

       ea = types[0]
       self.assertEqual(ea.xpath_needs_key, True)

   def test_mapping_site(self):
       types = JSSComputerAttributeType.objects.filter(label__exact='Site')
       self.assertEqual(types.count(),1)

       site = types[0]
       self.assertEqual(site.xpath_needs_key, False)
       self.assertEqual(site.computer_xpath, '//computer/general/site/name/text()')
  
   def test_mapping_building(self):
       types = JSSComputerAttributeType.objects.filter(label__exact='Building')
       self.assertEqual(types.count(),1)

       building = types[0]
       self.assertEqual(building.xpath_needs_key, False)
       self.assertEqual(building.api_path, '/api/url')
  
   def test_mapping_department(self):
       types = JSSComputerAttributeType.objects.filter(label__exact='Department')
       self.assertEqual(types.count(),1)

       dept = types[0]
       self.assertEqual(dept.xpath_needs_key, False)
       self.assertEqual(dept.api_path, '/api/url')

   def test_mappings_present(self):
       attribute_types = JSSComputerAttributeType.objects.all()
       self.assertEqual(attribute_types.count(),5)

class JSSComputerAttributeMappingTest(TestCase):

    fixtures = [ 'mapping_types', 'test_user', 'test_sites', ]


    def test_create_mapping_manifest(self):
        types = JSSComputerAttributeType.objects.filter(label__exact='Extension Attribute')
        self.assertEqual(types.count(),1)

        sites = JSSSite.objects.filter(jsssitename__exact='Full Site Access')
        self.assertEqual(sites.count(),1)

        obj = JSSComputerAttributeMapping.objects.create(
            jss_computer_attribute_type = types[0],
            jss_computer_attribute_key = 'Test extension attribute',
            jss_computer_attribute_value = 'Test value',
            manifest_element_type = 'm', 
            manifest_name = 'test_manifest',
            remove_from_xml = 0,
            jsssite=sites[0])

    def test_create_mapping_package(self):
        types = JSSComputerAttributeType.objects.filter(label__exact='Site')
        self.assertEqual(types.count(),1)

        sites = JSSSite.objects.filter(jsssitename__exact='Test site')
        self.assertEqual(sites.count(),1)

        obj = JSSComputerAttributeMapping.objects.create(
            jss_computer_attribute_type = types[0],
            jss_computer_attribute_key = '',
            jss_computer_attribute_value = 'Test Site',
            manifest_element_type = 'p', 
            manifest_name = 'test package',
            remove_from_xml = 0,
            jsssite=sites[0])

    def test_create_mapping_catalog(self):
        types = JSSComputerAttributeType.objects.filter(label__exact='Building')
        self.assertEqual(types.count(),1)

        sites = JSSSite.objects.filter(jsssitename__exact='Test site')
        self.assertEqual(sites.count(),1)

        obj = JSSComputerAttributeMapping.objects.create(
            jss_computer_attribute_type = types[0],
            jss_computer_attribute_key = '',
            jss_computer_attribute_value = 'Current Building',
            manifest_element_type = 'c', 
            manifest_name = 'test_catalog',
            remove_from_xml = 0,
            jsssite=sites[0])

    def test_create_mapping_empty(self):
        with self.assertRaisesMessage(IntegrityError, '(1048, "Column \'jss_computer_attribute_type_id\' cannot be null")'): JSSComputerAttributeMapping.objects.create()
       
@override_settings(MUNKI_REPO_DIR=cwd + '/' + test_repo_dir )
class JSSComputerAttributeMappingFormTest(TestCase):

    fixtures = [ 'mapping_types', 'test_user', 'test_sites', 'test_mappings',  ]

    def setUp(self):
        self.client = Client()

    def test_can_login_as_admin(self):
        rc = self.client.login(username='superted', password='superted')
        self.assertEqual(rc, True)
        rc = self.client.logout()

    def test_can_login_as_staffuser(self):
        rc = self.client.login(username='bananaman', password='bananaman')
        self.assertEqual(rc, True)
        rc = self.client.logout()

    def test_can_login_as_user(self):
        rc = self.client.login(username='mortal', password='mortal')
        self.assertEqual(rc, True)
        rc = self.client.logout()

    def test_can_client_needs_login(self):
        rc = self.client.get('/admin/jssmanifests/')

        self.assertEqual(rc.status_code, 302)
        self.assertEqual(rc.has_header('Location'), True)
        self.assertEqual(rc.get('Location'), 'http://testserver/admin/login/?next=/admin/jssmanifests/')

    def test_can_xml_without_login(self):
  
        sitedefault = open('jssmanifests/example-data/repo/manifests/site_default')
        sitedefault_content = sitedefault.read()

        rc = self.client.get('/jssmanifests/xml/site_default')
        self.assertEqual(rc.status_code, 200)

        self.assertEqual(rc.content, sitedefault_content) # how do we introduce tests ?
  
@override_settings(MUNKI_REPO_DIR=cwd + '/' + test_repo_dir )
class JSSComputerManifestTests(TestCase):

    fixtures = [ 'mapping_types', 'test_sites', 'test_mappings', ]

    def setUp(self):
        self.client = Client()

        computer_xml_file = open('jssmanifests/example-data/00000000-0000-1000-8000-000C29CDACC7')
        self.computer = etree.fromstring( computer_xml_file.read() )


    # Because I had some issues with this ...
    def test_override(self):
        self.assertEqual(settings.MUNKI_REPO_DIR,  cwd + '/' + test_repo_dir )

    def test_extension_attribute_mappings_ea(self):
        mapping_match = JSSComputerAttributeMapping.objects.get(id=1)
        self.assertEqual(mapping_match.computer_match(self.computer), True) 

        mapping_mismatch = JSSComputerAttributeMapping.objects.get(id=4)
        self.assertEqual(mapping_mismatch.computer_match(self.computer), False) 

        assert_test = {} # empty manifest, so be lazy
        assert_test['catalogs'] = []
        assert_test['catalogs'].append('ea_match_catalog')

        test_manifest = {}
        mapping_mismatch.apply_mapping(test_manifest)
        self.assertEqual(test_manifest, assert_test )

        assert_test = Manifest.read('site_default')
        assert_test['catalogs'].append('ea_match_catalog')

        test_manifest = Manifest.read('site_default')
        mapping_match.apply_mapping(test_manifest)

    def test_site_mappings(self):
        mapping_match = JSSComputerAttributeMapping.objects.get(id=2)
        self.assertEqual(mapping_match.computer_match(self.computer), True) 

        mapping_mismatch = JSSComputerAttributeMapping.objects.get(id=5)
        self.assertEqual(mapping_mismatch.computer_match(self.computer), False) 

        assert_test = {} # empty manifest, so be lazy
        assert_test['included_manifests'] = []
        assert_test['included_manifests'].append('site_match_manifest')

        test_manifest = {}
        mapping_mismatch.apply_mapping(test_manifest)
        self.assertEqual(test_manifest, assert_test)

        assert_test = Manifest.read('site_default')
        assert_test['included_manifests'].append('site_match_manifest')

        test_manifest = Manifest.read('site_default')
        mapping_match.apply_mapping(test_manifest)

        self.assertEqual(test_manifest, assert_test )

    def test_department_mappings(self):
        mapping_match = JSSComputerAttributeMapping.objects.get(id=3)
        self.assertEqual(mapping_match.computer_match(self.computer), True) 

        mapping_mismatch = JSSComputerAttributeMapping.objects.get(id=6)
        self.assertEqual(mapping_mismatch.computer_match(self.computer), False) 

        assert_test = {} # empty manifest, so be lazy
        assert_test['managed_installs'] = []
        assert_test['managed_installs'].append('department_one_package')

        test_manifest = {}
        mapping_mismatch.apply_mapping(test_manifest)
        self.assertEqual(test_manifest, assert_test)

        assert_test = Manifest.read('site_default')
        assert_test['managed_installs'].append('department_one_package')

        test_manifest = Manifest.read('site_default')
        mapping_match.apply_mapping(test_manifest)

        self.assertEqual(test_manifest, assert_test )

    def test_building_mappings(self):
        mapping_match = JSSComputerAttributeMapping.objects.get(id=7)
        self.assertEqual(mapping_match.computer_match(self.computer), True) 

        mapping_mismatch = JSSComputerAttributeMapping.objects.get(id=8)
        self.assertEqual(mapping_mismatch.computer_match(self.computer), False) 

        assert_test = {} # empty manifest, so be lazy
        assert_test['optional_installs'] = []
        assert_test['optional_installs'].append('building_two_package')

        test_manifest = {}
        mapping_mismatch.apply_mapping(test_manifest)
        self.assertEqual(test_manifest, assert_test)

        assert_test = Manifest.read('site_default')
        assert_test['optional_installs'].append('building_two_package')

        test_manifest = Manifest.read('site_default')
        mapping_match.apply_mapping(test_manifest)

        self.assertEqual(test_manifest, assert_test )

    def test_groups_mappings(self):
        mapping_match = JSSComputerAttributeMapping.objects.get(id=9)
        self.assertEqual(mapping_match.computer_match(self.computer), True) 

        mapping_mismatch = JSSComputerAttributeMapping.objects.get(id=10)
        self.assertEqual(mapping_mismatch.computer_match(self.computer), False) 

        assert_test = {} # empty manifest, so be lazy
        assert_test['managed_uninstalls'] = []
        assert_test['managed_uninstalls'].append('group_package')

        test_manifest = {}
        mapping_mismatch.apply_mapping(test_manifest)
        self.assertEqual(test_manifest, assert_test)

        assert_test = Manifest.read('site_default')
        assert_test['managed_uninstalls'].append('group_package')

        test_manifest = Manifest.read('site_default')
        mapping_match.apply_mapping(test_manifest)

        self.assertEqual(test_manifest, assert_test )


@override_settings(MUNKI_REPO_DIR=cwd + '/' + test_repo_dir )
class JSSComputerMappingFormDynamicContentTests(TestCase):

    fixtures = [ 'mapping_types', 'test_user', 'test_sites', 'test_mappings',  ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='superted', password='superted')

        # Add a mapping with a non-existant manifest
        
        types = JSSComputerAttributeType.objects.filter(label__exact='Extension Attribute')
        self.assertEqual(types.count(),1)

        sites = JSSSite.objects.filter(jsssitename__exact='Test site')
        self.assertEqual(sites.count(),1)

        obj = JSSComputerAttributeMapping.objects.create(
            jss_computer_attribute_type = types[0],
            jss_computer_attribute_key = 'Test extension attribute',
            jss_computer_attribute_value = 'Test value',
            manifest_element_type = 'm', 
            manifest_name = 'this manifest does not exist',
            remove_from_xml = 0,
            jsssite=sites[0])

        self.mapping_id = obj.id

    def test_mapping_exists(self):

        url = '/admin/jssmanifests/jsscomputerattributemapping/%s/'
        response = self.client.get(url % self.mapping_id )

        self.assertEqual(200, response.status_code)
        
        self.assertContains(response, "site_default</option>")
        self.assertContains(response, "this manifest does not exist</option>")



# 
#cwd = os.path.dirname(os.path.abspath(__file__))


# Later ....
if settings.JSS_URL and settings.JSS_CAN_USE_FOR_TESTS:

    class JSSSimulatedTests(TestCase):

         def test_one(self):
            self.assertEqual(1+1, 2)


