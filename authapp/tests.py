from django.test import TestCase

from authapp import models


class ModelTest(TestCase):

    def test_user_model_create_user(self):
        user = models.User.objects.create_user("user", "UserPassword")
        created_user = models.User.objects.latest("id")
        self.assertEqual(user, created_user)

    def test_user_model_create_superuser(self):
        superuser = models.User.objects.create_user("admin", "AdminPassword")
        created_superuser = models.User.objects.latest("id")
        self.assertEqual(superuser, created_superuser)

    def test_user_block_users(self):
        usernames = [f"user{i}" for i in range(1000)]
        for i in usernames:
            models.User.objects.create_user(i)
        models.User.objects.block_users(usernames)
        users_is_active = []
        for i in usernames:
            users_is_active.append(models.User.objects.get(username = i).is_active)
        self.assertEqual(users_is_active, [False] * len(usernames))

    def test_user_unlock_users(self):
        usernames = [f"user{i}" for i in range(1000)]
        for i in usernames:
            models.User.objects.create_user(i)
        models.User.objects.block_users(usernames)
        models.User.objects.unlock_users(usernames)
        users_is_active = []
        for i in usernames:
            users_is_active.append(models.User.objects.get(username = i).is_active)
        self.assertEqual(users_is_active, [True] * len(usernames))
