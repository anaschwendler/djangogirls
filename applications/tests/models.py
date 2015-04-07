from django.test import TestCase

from core.models import Event, EventPage
from applications.models import Form, Application, Question
from applications.utils import DEFAULT_QUESTIONS

class FormModel(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')

    def test_adding_default_questions(self):
        # Each new form should automatically create default questions
        form = Form.objects.create(page=self.page)
        self.assertEqual(form.question_set.count(), len(DEFAULT_QUESTIONS))

        # If you update the form, the default questions shouldn't be added
        form.text_header = 'Test'
        form.save()
        self.assertEqual(form.question_set.count(), len(DEFAULT_QUESTIONS))

    def test_number_of_applications(self):
        form = Form.objects.create(page=self.page)
        self.assertEqual(form.application_set.count(), form.number_of_applications)

        Application.objects.create(form=form)
        self.assertEqual(form.application_set.count(), form.number_of_applications)
        self.assertEqual(form.application_set.count(), 1)


class QuestionModel(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = Form.objects.create(page=self.page)

    def test_get_choices_as_list(self):
        # correctly return choices of a choices field
        question = Question.objects.filter(question_type='choices')[:1].get()
        self.assertEqual(sorted(question.get_choices_as_list()), sorted(question.choices.split(';')))

        # return TypeError if field is not a choices field
        question = Question.objects.filter(question_type='paragraph')[:1].get()
        with self.assertRaises(TypeError):
            question.get_choices_as_list()