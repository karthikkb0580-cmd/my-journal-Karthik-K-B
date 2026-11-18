from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    """One-to-Many: many articles can belong to one author.
    Many-to-Many: one article can have many categories.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="articles",
    )
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="articles",
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("journal:article_detail", kwargs={"pk": self.pk})

