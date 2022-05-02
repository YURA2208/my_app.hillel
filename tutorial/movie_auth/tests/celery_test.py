from django.test import TestCase
from movie_auth.models import MyUser
from movie_auth.tasks import notify_task_user


class TasksTestCase(TestCase):
    @classmethod
    def CreateUserTestCase(cls):
        MyUser.objects.create(
            username="iron man",
            email="ironman@gmail.com",
            password="Tanos",
            dob="1985-26-03"
        )

    def test_notify_task_user(self):
        for user in MyUser.objects.all():
            self.assertTrue(user.is_notified)
        self.assertEqual(notify_task_user(), "All users are notified")

