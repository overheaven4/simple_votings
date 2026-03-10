from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Voting, VotingOption, Vote
from django.utils import timezone

class VotingModelTest(TestCase):
    def setUp(self):
        # Подготовка данных для тестов
        self.user = User.objects.create_user(
            username='testuser_qa',
            password='testpassword'
        )
        self.voting = Voting.objects.create(
            title='Лучший язык программирования?',
            description='Голосуем за лучший ЯП 2024 года',
            creator=self.user
        )
        self.option1 = VotingOption.objects.create(
            voting=self.voting,
            text='Python'
        )
        self.option2 = VotingOption.objects.create(
            voting=self.voting,
            text='JavaScript'
        )

    def test_voting_creation(self):
        self.assertEqual(self.voting.title, 'Лучший язык программирования?')
        self.assertEqual(self.voting.creator.username, 'testuser_qa')
        self.assertTrue(self.voting.created_at <= timezone.now())

    def test_voting_option_creation(self):
        self.assertEqual(self.option1.text, 'Python')
        self.assertEqual(self.option1.voting, self.voting)
        self.assertEqual(str(self.option1), 'Python')

    def test_vote_creation(self):
        vote = Vote.objects.create(
            option=self.option1,
            user=self.user
        )
        self.assertEqual(vote.option, self.option1)
        self.assertEqual(vote.user, self.user)
        self.assertTrue(vote.created_at <= timezone.now())
        self.assertEqual(Vote.objects.count(), 1)