from django.test import TestCase, override_settings
from django.test import Client
from django.conf import settings
from django.db.utils import IntegrityError

import os

from jssmanifests.models import JSSComputerAttributeType,JSSComputerAttributeMapping

# Create your tests here.

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

    fixtures = [ 'mapping_types', 'test_user', ]


    def test_create_mapping_manifest(self):
        types = JSSComputerAttributeType.objects.filter(label__exact='Extension Attribute')
        self.assertEqual(types.count(),1)

        obj = JSSComputerAttributeMapping.objects.create(
            jss_computer_attribute_type = types[0],
            jss_computer_attribute_key = 'Test extension attribute',
            jss_computer_attribute_value = 'Test value',
            manifest_element_type = 'm', 
            manifest_name = 'test_manifest',
            remove_from_xml = 0)

    def test_create_mapping_package(self):
        types = JSSComputerAttributeType.objects.filter(label__exact='Site')
        self.assertEqual(types.count(),1)

        obj = JSSComputerAttributeMapping.objects.create(
            jss_computer_attribute_type = types[0],
            jss_computer_attribute_key = '',
            jss_computer_attribute_value = 'Test Site',
            manifest_element_type = 'p', 
            manifest_name = 'test package',
            remove_from_xml = 0)

    def test_create_mapping_catalog(self):
        types = JSSComputerAttributeType.objects.filter(label__exact='Building')
        self.assertEqual(types.count(),1)

        obj = JSSComputerAttributeMapping.objects.create(
            jss_computer_attribute_type = types[0],
            jss_computer_attribute_key = '',
            jss_computer_attribute_value = 'Current Building',
            manifest_element_type = 'c', 
            manifest_name = 'test_catalog',
            remove_from_xml = 0)

    def test_create_mapping_empty(self):

        with self.assertRaisesMessage(IntegrityError, '(1048, "Column \'jss_computer_attribute_type_id\' cannot be null")'): JSSComputerAttributeMapping.objects.create()
       
# 
cwd = os.path.dirname(os.path.abspath(__file__))
test_repo_dir = 'example-data/repo/'
@override_settings(MUNKI_REPO_DIR=cwd + '/' + test_repo_dir )
class JSSComputerAttributeMappingFormTest(TestCase):

    fixtures = [ 'mapping_types', 'test_user', ]

    def setUp(self):
        self.client = Client()

    # Because I had some issues with this ...
    def test_override(self):
        self.assertEqual(settings.MUNKI_REPO_DIR,  cwd + '/' + test_repo_dir )

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
   
  
        sitedefault = open('jssmanifests/example-data/repo/manifests/site_default')
        sitedefault_content = sitedefault.read()
        # However, jss manifests do not need auth
        rc = self.client.get('/jssmanifests/xml/site_default')
        self.assertEqual(rc.status_code, 200)
        self.assertEqual(rc.content, sitedefault_content) # how do we introduce tests ?



# Later ....
if settings.JSS_URL and settings.JSS_CAN_USE_FOR_TESTS:

    class JSSSimulatedTests(TestCase):

         def test_one(self):
            self.assertEqual(1+1, 2)


