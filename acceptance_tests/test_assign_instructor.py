from django.test import TestCase
from django.test.client import Client
from django.contrib.messages import get_messages
from ta_assign import models


class AssignInstructorTests(TestCase):

    def setUp(self):
        return

    def test_no_login_get(self):

        client = Client()
        response = client.get('/assign_instructor/')
        # this gets any messages
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # this should be the first and only message, tagged error
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "Please login first.")
        # since we returned a redirect, we can check the location
        self.assertEqual(response.get('location'), '/login/')

    def test_instructor_get(self):

        client = Client()
        session = client.session
        session['email'] = 'inst@uwm.edu'
        session['type'] = 'instructor'
        session.save()
        response = client.get('/assign_instructor/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_ta_get(self):

        client = Client()
        session = client.session
        session['email'] = 'ta@uwm.edu'
        session['type'] = 'ta'
        session.save()
        response = client.get('/assign_instructor/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_admin_get(self):

        client = Client()
        session = client.session
        session['email'] = 'admin@uwm.edu'
        session['type'] = 'administrator'
        session.save()
        response = client.get('/assign_instructor/')
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        self.assertEqual(all_messages[0].tags, "error")
        self.assertEqual(all_messages[0].message, "You do not have access to this page.")
        self.assertEqual(response.get('location'), '/index/')

    def test_sup_get(self):

        client = Client()
        # make a session, email and type are all you need
        session = client.session
        session['email'] = 'sup@uwm.edu'
        session['type'] = 'supervisor'
        # save the session
        session.save()
        response = client.get('/assign_instructor/')
        # status code 200, we loaded the correct page
        self.assertEqual(response.status_code, 200)
        # since we returned a render, it has all the content of the page
        # we'll just look for the header
        self.assertContains(response, "Assign Instructor")
        all_messages = [msg for msg in get_messages(response.wsgi_request)]
        # no error messages
        self.assertEqual(len(all_messages), 0)

    def test_super_post(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_instructor/', data={'email': "instructor@uwm.edu", 'course_id': "301",
                                                         'course_department': "COMPSCI"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign Instructor")
        self.assertContains(response, "Instructor Assigned!")

    def test_invalid_instructor(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_instructor/', data={'email': "ins@uwm.edu", 'course_id': "301",
                                                            'course_department': "COMPSCI"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign Instructor")
        self.assertContains(response, "no such instructor")

    def test_invalid_course(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_instructor/', data={'email': "instructor@uwm.edu", 'course_id': "302",
                                                            'course_department': "COMPSCI"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign Instructor")
        self.assertContains(response, "no such course")

    def test_invalid_dept(self):
        inst1 = models.User()
        inst1.email = "instructor@uwm.edu"
        inst1.type = "instructor"
        inst1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_instructor/', data={'email': "instructor@uwm.edu", 'course_id': "301",
                                                            'course_department': "PHYSICS"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign Instructor")
        self.assertContains(response, "no such course")

    def test_assign_improper_ta(self):
        ta1 = models.User()
        ta1.email = "ta@uwm.edu"
        ta1.type = "ta"
        ta1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_instructor/', data={'email': "ta@uwm.edu", 'course_id': "301",
                                                            'course_department': "COMPSCI"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign Instructor")
        self.assertContains(response, "no such instructor")

    def test_assign_improper_admin(self):
        ad1 = models.User()
        ad1.email = "admin@uwm.edu"
        ad1.type = "administrator"
        ad1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_instructor/', data={'email': "admin@uwm.edu", 'course_id': "301",
                                                            'course_department': "COMPSCI"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign Instructor")
        self.assertContains(response, "no such instructor")

    def test_assign_improper_sup(self):
        sup1 = models.User()
        sup1.email = "sup@uwm.edu"
        sup1.type = "supervisor"
        sup1.save()

        course = models.Course()
        course.num_labs = 2
        course.current_num_TA = 0
        course.num_lectures = 1
        course.instructor = "DEFAULT"
        course.course_id = "301"
        course.course_department = "COMPSCI"
        course.save()

        client = Client()
        session = client.session
        session['email'] = 'ta_assign_super@uwm.edu'
        session['type'] = 'supervisor'
        session.save()
        response = client.post('/assign_instructor/', data={'email': "sup@uwm.edu", 'course_id': "301",
                                                            'course_department': "COMPSCI"}, follow="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assign Instructor")
        self.assertContains(response, "no such instructor")