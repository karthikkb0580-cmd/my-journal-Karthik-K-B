from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import Profile

User = get_user_model()


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="learner", password="Strong-password-12345")

    def test_profile_is_one_to_one(self):
        profile = Profile.objects.create(user=self.user, display_name="Learner")
        self.assertEqual(self.user.profile, profile)

    def test_registration_creates_account_and_profile(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newlearner",
            "password1": "Another-strong-password-12345",
            "password2": "Another-strong-password-12345",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newlearner").exists())
        self.assertTrue(Profile.objects.filter(user__username="newlearner").exists())

    def test_normal_user_cannot_open_editor_area(self):
        self.client.login(username="learner", password="Strong-password-12345")
        response = self.client.get(reverse("accounts:editor_area"))
        self.assertEqual(response.status_code, 302)

    def test_content_editor_group_can_open_editor_area(self):
        group, _ = Group.objects.get_or_create(name="ContentEditors")
        self.user.groups.add(group)
        self.client.login(username="learner", password="Strong-password-12345")
        response = self.client.get(reverse("accounts:editor_area"))
        self.assertEqual(response.status_code, 200)
