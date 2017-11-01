from django.test import TestCase, Client
from sio.models import *

# /sio/create-student (andrew_id, first_name, last_name)

class CreateStudentModelsTest(TestCase):
    fixtures = ['sample-data']

    def test_add_student(self):    # Tests the to-do list add-item function.
        self.assertTrue(Student.objects.all().count() == 0)
        new_item = Student(andrew_id='nfajriya', first_name='nurlaili', last_name='fajriyah')
        new_item.save()
        self.assertTrue(Student.objects.all().count() == 1)

class SioTest(TestCase):
    def test_create_student(self):
        client = Client()       # add-item expects a POST request with one
                                # query parameter, item, the text of the to-do
                                # list item.
        sample_andrew = 'nfajriya'
        sample_fn = 'nurlaili'
        sample_ln = 'fajriyah'

        response = client.post('/sio/create-student', {'andrew_id':sample_andrew})
        self.assertTrue(response.content.find(sample_student.encode()) >= 0)