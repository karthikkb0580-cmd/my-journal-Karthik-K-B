from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Article, Category

User = get_user_model()


class JournalTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="Strong-password-12345")
        self.other = User.objects.create_user(username="other", password="Other-strong-password-12345")
        self.article = Article.objects.create(
            author=self.author,
            title="A useful Django article",
            body="This is a sufficiently long article body.",
            is_published=True,
        )

    def test_home_page_returns_success(self):
        response = self.client.get(reverse("journal:home"))
        self.assertEqual(response.status_code, 200)

    def test_published_article_is_listed(self):
        response = self.client.get(reverse("journal:article_list"))
        self.assertContains(response, self.article.title)

    def test_draft_article_is_not_public(self):
        draft = Article.objects.create(
            author=self.author,
            title="Private draft",
            body="This draft should not be visible publicly.",
            is_published=False,
        )
        response = self.client.get(reverse("journal:article_list"))
        self.assertNotContains(response, draft.title)

    def test_logged_out_user_cannot_create_article(self):
        response = self.client.get(reverse("journal:article_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_author_can_update_own_article(self):
        self.client.login(username="author", password="Strong-password-12345")
        response = self.client.post(
            reverse("journal:article_update", args=[self.article.pk]),
            {
                "title": "Updated Django title",
                "subtitle": "",
                "body": "This updated body is long enough.",
                "is_published": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Updated Django title")

    def test_user_cannot_update_another_users_article(self):
        self.client.login(username="other", password="Other-strong-password-12345")
        response = self.client.get(reverse("journal:article_update", args=[self.article.pk]))
        self.assertEqual(response.status_code, 404)

    def test_many_to_many_categories(self):
        first = Category.objects.create(name="Django")
        second = Category.objects.create(name="Database")
        self.article.categories.add(first, second)
        self.assertEqual(self.article.categories.count(), 2)

    def test_search_filters_articles(self):
        response = self.client.get(reverse("journal:article_list"), {"q": "useful"})
        self.assertContains(response, self.article.title)
