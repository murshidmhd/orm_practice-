from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"
        indexes = [
            models.Index(
                fields=[
                    "-created_at",
                ]
            ),
            models.Index(
                fields=[
                    "-is_active",
                ]
            ),
        ]

    def __str__(self):
        return f"{self.__class__.__name__}: {getattr(self, 'title', getattr(self, 'name', self.id))}"


class Author(TimeStampedModel):
    name = models.CharField(max_length=100)
    book_written = models.PositiveIntegerField(default=0, editable=False)



class Publisher(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class PublishedBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def recent(self, count=5):
        return self.get_queryset().order_by("-created_at")[:count]


class Book(TimeStampedModel):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="publisher"
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateField(default=timezone.now)

    published = PublishedBookManager()
    objects = models.Manager()

    # def __str__(self):
    #     return f"{self.title}"

    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "Books"

        get_latest_by = "created_at"
        indexes = [
            models.Index(fields=["is_published"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["author", "is_published"]),
        ]

    # indeces make fast just like if we have 500 ms program it will run with 5ms time


class PublishedBook(Book):
    class Meta:
        proxy = True

    def __str__(self):
        return f"PUBLISHED:{self.title}"

    def congratulate(self):
        return f"Congratulations!' {self.title}' is now live!"


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
