from django.test import TestCase
from .models import Subject,Student,registerSubject

class StudentTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create(username="6510615047")
    
    def test_student_creation(self):
        self.assertEqual(self.student.username, '6510615047')

    def test_student_max_length(self):
        username_field = Student._meta.get_field('username')
        max_length = username_field.max_length
        self.assertFalse(max_length > 10)
        
class SubjectTestCase(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(subjectCode='CN331',
                                               subjectName= 'Software Engineering',
                                               semester = 1,
                                               year = 3,
                                               seatAvailable = 2,
                                               status = 'open')
    
    def test_subject_creation(self):
        self.assertEqual(self.subject.subjectCode,'CN331')
        self.assertEqual(self.subject.subjectName, 'Software Engineering')
        self.assertEqual(self.subject.semester, 1)
        self.assertEqual(self.subject.year, 3)
        self.assertEqual(self.subject.seatAvailable, 2)
        self.assertEqual(self.subject.status, 'open')

    def test_subject_max_length(self):
        subjectCode = Subject._meta.get_field('subjectCode')
        subjectName = Subject._meta.get_field('subjectName')
        status = Subject._meta.get_field('status')
        subjectCode_max_length = subjectCode.max_length
        subjectName_max_length = subjectName.max_length
        status_max_length = status.max_length
        self.assertFalse(subjectCode_max_length > 10)
        self.assertFalse(subjectName_max_length > 50)
        self.assertFalse(status_max_length > 10)
    
    def test_subject_str_method(self):
        expected_str = "(CN331)  Software Engineering"
        self.assertEqual(str(self.subject), expected_str)
    
class registerSubjectTestCase(TestCase):
    def setUp(self):
        self.registerSubject = registerSubject.objects.create(username = "6510615047",
                                                              subjectCode = "CN331",
                                                              subjectName= 'Software Engineering',
                                                              semester = 1,
                                                              year = 3)
    
    def test_registerSubject_creation(self):
        self.assertEqual(self.registerSubject.subjectCode,'CN331')
        self.assertEqual(self.registerSubject.subjectName, 'Software Engineering')
        self.assertEqual(self.registerSubject.semester, 1)
        self.assertEqual(self.registerSubject.year, 3)
    
    def test_registerSubject_max_length(self):
        username = registerSubject._meta.get_field('username')
        subjectCode = registerSubject._meta.get_field('subjectCode')
        subjectName = registerSubject._meta.get_field('subjectName')
        username_max_length = username.max_length
        subjectCode_max_length = subjectCode.max_length
        subjectName_max_length = subjectName.max_length
        self.assertFalse(username_max_length > 10)
        self.assertFalse(subjectCode_max_length > 10)
        self.assertFalse(subjectName_max_length > 50)

    def test_registerSubject_str_method(self):
        expected_str = "Software Engineering (CN331) (6510615047)"
        self.assertEqual(str(self.registerSubject), expected_str)