from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AccountViewTests(TestCase):
	def test_signup_shows_success_message(self):
		response = self.client.post(reverse("signup"), {
			"username": "newstudent",
			"email": "student@example.com",
			"first_name": "New",
			"last_name": "Student",
			"course": "CSIT",
			"password1": "CampusPass!8642",
			"password2": "CampusPass!8642",
		}, follow=True)

		self.assertContains(response, "Your account has been created successfully!")
		self.assertRedirects(response, reverse("login"))

	def test_profile_update_saves_current_user(self):
		user = get_user_model().objects.create_user(
			username="student",
			password="CampusPass!8642",
		)
		self.client.force_login(user)

		response = self.client.post(reverse("profile"), {
			"first_name": "Updated",
			"last_name": "Student",
			"email": "updated@example.com",
			"course": "CSIT",
		}, follow=True)

		user.refresh_from_db()
		self.assertEqual(user.first_name, "Updated")
		self.assertEqual(user.email, "updated@example.com")
		self.assertContains(response, "Your profile has been updated.")
