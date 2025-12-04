from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class PublishedBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def recent(self, count=5):
        return self.get_queryset().order_by("-created_at")[:count]


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="publisher"
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now)

    published = PublishedBookManager()
    objects = models.Manager()

    def __str__(self):
        return f"{self.title}"


class review(models.Model):
    Book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )

    rating = models.IntegerField()
    text = models.TextField()


# When creating a custom manager, we override get_queryset() because Django calls it every time the manager is used.
# We use super().get_queryset() to get the original queryset from models.Manager, then chain our filter — here is_published=True.
# This way, Book.published.any_method() will always only see published books.
# Then in helper methods like recent(), we call self.get_queryset() to reuse that filtered base instead of repeating the filter.
