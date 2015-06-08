from django.test import TestCase

# Create your tests here.

def test_login():
   response = client.get('/')
   if repsonse.status_code != 302: 
      print "error"

   if not response.has_header('Location'):
      print "error"

   if response.get('Location') != 'http://testserver/login/?next=/':
      print "Error"

   response = client.post('/login/?next=/', { 'user': 'admin', 'password': 'secret'} )

