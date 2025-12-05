from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Book


@receiver(post_save, sender=Book)
def update_author_book_count(sender, instance, created, **kwargs):
    author = instance.author

    published_count = author.books.filter(is_published=True).count()

    author.books_wrtten = published_count
    author.save(update_field=["books_written"])
