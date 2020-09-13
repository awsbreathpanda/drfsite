from polls.models import Choice, Question
from rest_framework.test import APITestCase
from rest_framework import status
import json


# Create your tests here.
class QuestionViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.question_1 = Question.objects.create(
            question_text='question_text_1?')
        self.question_2 = Question.objects.create(
            question_text='question_text_2?')

    def tearDown(self) -> None:
        self.question_1.delete()
        self.question_2.delete()

    def test_get_list(self):
        url = '/polls/questions/'

        rsp = self.client.get(url)
        content = json.loads(rsp.content)

        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 2)

    def test_get_detail(self):
        url = '/polls/questions/' + str(self.question_1.id) + '/'

        rsp = self.client.get(url)
        content = json.loads(rsp.content)

        # print('===>', content)
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get('question_text'),
                         self.question_1.question_text)

    def test_post(self):
        url = '/polls/questions/'

        rsp = self.client.post(url,
                               data={
                                   'question_text': 'question_text_3?',
                               })

        Question.objects.get(question_text='question_text_3?')
        self.assertEqual(rsp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 3)


class ChoiceViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.question = Question.objects.create(question_text='question_text?')
        self.choice_1 = Choice.objects.create(question=self.question,
                                              choice_text='choice_text_1',
                                              votes=0)
        self.choice_2 = Choice.objects.create(question=self.question,
                                              choice_text='choice_text_2',
                                              votes=0)

    def tearDown(self) -> None:
        self.question.delete()

    def test_get_list(self):
        url = '/polls/choices/'

        rsp = self.client.get(url)
        content = json.loads(rsp.content)

        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 2)

    def test_get_detail(self):
        url = '/polls/choices/' + str(self.choice_1.id) + '/'

        rsp = self.client.get(url)
        content = json.loads(rsp.content)

        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get('choice_text'), self.choice_1.choice_text)

    def test_post(self):
        url = '/polls/choices/'

        rsp = self.client.post(url,
                               data={
                                   'question':
                                   'http://localhost:8000/polls/questions/' +
                                   str(self.question.id) + '/',
                                   'choice_text':
                                   'choice_text_3',
                               })

        self.assertEqual(rsp.status_code, status.HTTP_201_CREATED)
        Choice.objects.get(choice_text='choice_text_3')
        self.assertEqual(Choice.objects.count(), 3)
