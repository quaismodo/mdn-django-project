from django.shortcuts import render

from .models import Book, Genre, BookInstance, Author


# Create your views here.
def index(request):
    """
    Функция для отображения домашней страницы сайта.
    :param request:
    :return:
    """
    # Генерация количеств некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Доступные книги (статус = 'а')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Количество жанров
    num_genres = Genre.objects.count()

    # Количество книг, содержащих слово War без учета регистра
    num_matches_books = Book.objects.filter(title__icontains='war').count()

    return render(request,
                  'index.html',
                  context={
                      'num_books': num_books,
                      'num_instances': num_instances,
                      'num_instances_available': num_instances_available,
                      'num_authors': num_authors,
                      'num_genres': num_genres,
                      'num_matches_books': num_matches_books, }, )
