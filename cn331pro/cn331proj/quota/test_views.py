from django.test import TestCase
from django.urls import reverse
from .models import Student, Subject, registerSubject
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

class quotaUrlTestCase(TestCase):
    def test_default_status_code(self):
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)

    def test_subject_list_status_code(self):
        response = self.client.get(reverse('subject_list')) 
        self.assertEqual(response.status_code, 200)

    def test_my_quota_status_code(self):
        response = self.client.get(reverse('my_quota')) 
        self.assertEqual(response.status_code, 200)

class AddSubjectViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="6510615000", password="ajarnjack")
        self.subject_with_seats = Subject.objects.create(
            subjectCode='CN350',
            subjectName='Cryptography',
            semester=1,
            year=2024,
            seatAvailable=2,
            status='Open'
        )
        self.subject_no_seats = Subject.objects.create(
            subjectCode='CN361',
            subjectName='Microprocessor ',
            semester=1,
            year=2024,
            seatAvailable=0,
            status='Close'
        )
    
    def test_add_subject_success(self):
        self.client.login(username="6510615000", password="ajarnjack")
        
        response = self.client.get(reverse('add_subject', args=[self.subject_with_seats.subjectCode]))
        
        self.assertTrue(registerSubject.objects.filter(username=self.user.username, subjectCode='CN350').exists())
        
        self.subject_with_seats.refresh_from_db()
        self.assertEqual(self.subject_with_seats.seatAvailable, 1)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Subject CN350 has been added to your quota." in str(message) for message in messages))
        
        self.assertRedirects(response, reverse('my_quota'))

    def test_add_subject_no_seats_available(self):
        self.client.login(username="6510615000", password="ajarnjack")
        
        response = self.client.get(reverse('add_subject', args=[self.subject_no_seats.subjectCode]))
        
        self.assertFalse(registerSubject.objects.filter(username=self.user.username, subjectCode='CS361').exists())
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("No seats available for this subject." in str(message) for message in messages))
        
        self.assertRedirects(response, reverse('my_quota'))

       
    def test_add_subject_already_added(self):
        registerSubject.objects.create(
        username=self.user.username,
        subjectCode='CN350',  
        subjectName='Cryptography',
        semester=1,
        year=2024,
        )

        self.client.login(username="6510615000", password="ajarnjack")
    
        response = self.client.get(reverse('add_subject', args=[self.subject_with_seats.subjectCode]))
    
        self.assertEqual(registerSubject.objects.filter(username=self.user.username, subjectCode='CN350').count(), 1)
    
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("This subject has already been added to your quota." in str(message) for message in messages))
    
        self.assertRedirects(response, reverse('my_quota'))
    
    def test_status_close(self):
        self.client.login(username="6510615000", password="ajarnjack")

        self.subject_with_seats.seatAvailable = 1
        self.subject_with_seats.save()

        response = self.client.get(reverse('add_subject', args=[self.subject_with_seats.subjectCode]))
        self.subject_with_seats.refresh_from_db()

        self.assertEqual(self.subject_with_seats.status, 'Close')

class DelSubjectViewTestsCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="6510615000", password="ajarnjack")
        self.subject_with_seats = Subject.objects.create(
            subjectCode='CN331',
            subjectName='Software Engineer',
            semester=1,
            year=2024,
            seatAvailable=2,
            status='Open'
        )
        self.subject_no_seats = Subject.objects.create(
            subjectCode='CN361',
            subjectName='Microprocessor ',
            semester=1,
            year=2024,
            seatAvailable=0,
            status='Close'
        )
    
    def test_del_subject_success(self):
        registerSubject.objects.create(
        username=self.user.username,
        subjectCode='CN331',  
        subjectName='Software Engineer',
        semester=1,
        year=2024,
        )
        self.client.login(username="6510615000", password="ajarnjack")

        self.assertTrue(registerSubject.objects.filter(username=self.user.username, subjectCode='CN331').exists())
        self.subject_with_seats.refresh_from_db()
        self.assertEqual(self.subject_with_seats.seatAvailable,2)

        response = self.client.get(reverse('del_subject', args=[self.subject_with_seats.subjectCode]))

        self.assertFalse(registerSubject.objects.filter(username=self.user.username, subjectCode='CN331').exists())
        self.subject_with_seats.refresh_from_db()
        self.assertEqual(self.subject_with_seats.seatAvailable,3)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Subject CN331 has been removed from your quota." in str(message) for message in messages))

        self.assertRedirects(response, reverse('my_quota'))
    
    def test_status_open(self):
        self.client.login(username="6510615000", password="ajarnjack")

        registerSubject.objects.create(
            username=self.user.username,
            subjectCode='CN361',
            subjectName='Microprocessor',
            semester=1,
            year=2024,
        )

        response = self.client.get(reverse('del_subject', args=[self.subject_no_seats.subjectCode]))
        self.subject_no_seats.refresh_from_db()

        self.assertEqual(self.subject_no_seats.status, 'Open')
        self.assertEqual(self.subject_no_seats.seatAvailable, 1)
