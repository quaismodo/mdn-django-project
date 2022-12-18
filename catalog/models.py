from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

from datetime import date

import uuid


# Create your models here.
class Genre(models.Model):
    """
    Model representing a book genre
    Модель, представляющая книжный жанр
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (Science Fiction)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        Строка для представления объекта модели (на сайте администратора и т.д.)
        :return:
        """
        return self.name


class Book(models.Model):
    """
    Model representing a book
    Модель, представляющая книгу
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/'
                                                             'conten/what-isbn>"ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select genre for this book")

    def __str__(self):
        """
        String for representing the Model object.
        Строка для представления объекта модели.
        :return:
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        Возвращает URL-адрес для доступа к конкретному экземпляру книги
        :return:
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        :return:
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book.
    Модель, представляющая конкретный экземпляр книги.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular"
                                                                          "book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reversed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]

        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String for representing the Model object
        Строка для представления объекта модели
        :return:
        """
        return '{id} {title}'.format(id=self.id, title=self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """
    Model representing an author.
    Модель, представляющая автора
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        Возвращает URL-адрес для доступа к конкретному экземпляру автора
        :return:
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        :return:
        """
        return '{last_name}, {first_name}'.format(last_name=self.last_name, first_name=self.first_name)
