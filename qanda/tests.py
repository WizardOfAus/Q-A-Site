from django.test import TestCase, Client
from django.utils import timezone
from qanda.models import Question, Answer, Profile
from qanda.forms import SignUpForm, QuestionForm, AnswerForm
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.
class QuestionModelTests(TestCase):
    def test___str__(self):
        q = Question(question_title="My question", question_body="AAA")
        self.assertEqual(str(q), "My question")


class AnswerModelTests(TestCase):
    def test___str__(self):
        q = Question(question_title="My question", question_body="AAA")
        time = timezone.now()
        a = Answer(answer_text="BBB", question_answered=q, pub_date=time)
        self.assertEqual(str(a), "Answer to My question published " + str(time))


class ProfileModelTests(TestCase):
    def test_when_user_is_saved_profile_is_created(self):
        u = User(first_name="Robert", last_name="Greener")
        u.save()
        self.assertNotEqual(None, u.profile)
        self.assertEqual(Profile, type(u.profile))


class SignupFormTests(TestCase):
    def test_form_with_valid_data(self):
        form_data = {
            'username': 'roberto',
            'first_name': 'Robert',
            'last_name': 'Greener',
            'email': 'robert.greener@kcl.ac.uk',
            'role': 'Undergraduate',
            'faculty': 'Faculty of Natural & Mathematical Sciences',
            'password1': 'alexander1',
            'password2': 'alexander1'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_email(self):
        form_data = {
            'username': 'roberto',
            'first_name': 'Robert',
            'last_name': 'Greener',
            'email': 'robert.greener@kcl',
            'role': 'Undergraduate',
            'faculty': 'Faculty of Natural & Mathematical Sciences',
            'password1': 'alexander1',
            'password2': 'alexander1'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_role_choice(self):
        form_data = {
            'username': 'roberto',
            'first_name': 'Robert',
            'last_name': 'Greener',
            'email': 'robert.greener@ucl.ac.uk',
            'role': 'Student',
            'faculty': 'Faculty of Natural & Mathematical Sciences',
            'password1': 'alexander1',
            'password2': 'alexander1'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_faculty_choice(self):
        form_data = {
            'username': 'roberto',
            'first_name': 'Robert',
            'last_name': 'Greener',
            'email': 'robert.greener@kcl.ac.uk',
            'role': 'Undergraduate',
            'faculty': 'Faculty of cool',
            'password1': 'alexander1',
            'password2': 'alexander1'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_non_matching_passwords(self):
        form_data = {
            'username': 'roberto',
            'first_name': 'Robert',
            'last_name': 'Greener',
            'email': 'robert.greener@kcl.ac.uk',
            'role': 'Undergraduate',
            'faculty': 'Faculty of Natural & Mathematical Sciences',
            'password1': 'alexander1',
            'password2': 'alexander2'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_non_kcl_email_account(self):
        form_data = {
            'username': 'roberto',
            'first_name': 'Robert',
            'last_name': 'Greener',
            'email': 'robert.greener@ucl.ac.uk',
            'role': 'Undergraduate',
            'faculty': 'Faculty of Natural & Mathematical Sciences',
            'password1': 'alexander1',
            'password2': 'alexander1'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())


class SignupViewTests(TestCase):
    def test_not_post(self):
        client = Client()
        response = client.get(reverse('qanda:signup'))
        self.assertEqual(200, response.status_code)

    def test_post_redirect(self):
        data = {
            'username': 'roberto',
            'first_name': 'Robert',
            'last_name': 'Greener',
            'email': 'robert.greener@kcl.ac.uk',
            'role': 'Undergraduate',
            'faculty': 'Faculty of Natural & Mathematical Sciences',
            'password1': 'alexander1',
            'password2': 'alexander1'
        }
        client = Client()
        response = client.post(reverse('qanda:signup'), data, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('/', response.redirect_chain[-1][0])
        self.assertEqual(302, response.redirect_chain[-1][1])

    def test_post_creates_user_IT(self):
        data = {
            'username': 'roberto',
            'first_name': 'Robert',
            'last_name': 'Greener',
            'email': 'robert.greener@kcl.ac.uk',
            'role': 'Undergraduate',
            'faculty': 'Faculty of Natural & Mathematical Sciences',
            'password1': 'alexander1',
            'password2': 'alexander1'
        }
        client = Client()
        client.post(reverse('qanda:signup'), data)
        u = User.objects.get(username="roberto")
        self.assertEqual("Robert", u.first_name)
        self.assertEqual("Undergraduate", u.profile.role)


class QuestionFormTests(TestCase):
    def test_form_with_valid_data(self):
        form = QuestionForm(data={
            'question_title': 'What is 2+2',
            'question_body': 'xxxxxxxxxxxxxx'
        })
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_data(self):
        form = QuestionForm(data={
            'question_title': 'a' * 201,
            'question_body': 'xxxxxxxxxxxxxx'
        })
        self.assertFalse(form.is_valid())


class AnswerFormTests(TestCase):
    def test_form_with_data(self):
        form = AnswerForm(data={
            'answer_text': 'a' * 1000
        })
        self.assertTrue(form.is_valid())


class PostQuestionViewTests(TestCase):
    def test_not_post(self):
        client = Client()
        response = client.get(reverse('qanda:post'))
        self.assertEqual(200, response.status_code)

    def test_post_redirect(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        data = {
            'question_body': 'a' * 250,
            'question_title': 'test12345'
        }
        response = client.post(reverse('qanda:post'), data, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(reverse('qanda:detail', args=(Question.objects.get(question_title='test12345').id,)), response.redirect_chain[-1][0])
        self.assertEqual(302, response.redirect_chain[-1][1])

    def test_post_creates_question_IT(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        data = {
            'question_body': 'a' * 250,
            'question_title': 'test12345'
        }
        client.post(reverse('qanda:post'), data)
        q = Question.objects.get(question_title='test12345')
        self.assertEqual('a' * 250, q.question_body)
        self.assertEqual('test12345', q.question_title)
        self.assertEqual(user.profile, q.author)

    def test_post_not_logged_in(self):
        client = Client()
        client.logout()
        data = {
            'question_body': 'a' * 250,
            'question_title': 'test12345'
        }
        self.assertEqual(403, client.post(reverse('qanda:post'), data).status_code)


class DetailViewTests(TestCase):
    def test_not_post(self):
        client = Client()
        q = Question(question_title="Xax", question_body="dddd")
        q.save()
        response = client.get(reverse('qanda:detail', args=(q.id,)))
        self.assertEqual(200, response.status_code)

    def test_post_redirect_valid(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        data = {
            'answer_text': 'a' * 100
        }
        q = Question(question_title="Xax", question_body="dddd")
        q.save()
        response = client.post(reverse('qanda:detail', args=(q.id,)), data=data, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(reverse('qanda:detail', args=(q.id,)), response.redirect_chain[-1][0])
        self.assertEqual(302, response.redirect_chain[-1][1])

    def test_post_redirect_invalid(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        data = {}
        q = Question(question_title="Xax", question_body="dddd")
        q.save()
        response = client.post(reverse('qanda:detail', args=(q.id,)), data=data, follow=True)
        self.assertEqual(0, len(response.redirect_chain))

    def test_post_creates_question_IT(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        data = {
            'answer_text': 'a' * 100
        }
        q = Question(question_title="Xax", question_body="dddd")
        q.save()
        response = client.post(reverse('qanda:detail', args=(q.id,)), data=data)
        a = q.answer_set.get(answer_text='a' * 100)
        self.assertEqual('a' * 100, a.answer_text)
        self.assertEqual(user.profile, a.author)

    def test_post_not_logged_in(self):
        client = Client()
        client.logout()
        data = {
            'answer_text': 'a' * 100
        }
        q = Question(question_title="Xax", question_body="dddd")
        q.save()
        response = client.post(reverse('qanda:detail', args=(q.id,)), data=data)
        self.assertEqual(403, response.status_code)
