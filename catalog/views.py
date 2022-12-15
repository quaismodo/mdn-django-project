from django.shortcuts import render

from .models import Book, Genre, BookInstance, Author

from django.views import generic


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


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    # context_object_name = 'my_book_list'
    # # ваше собственное имя переменной контекста в шаблоне
    # queryset = Book.objects.filter(title__icontains='war')[:5]
    # # получение 5 книг, содержащих слово war
    # template_name = 'books/my_arbitrary_template_name_list.html'
    # # Определение имени вашего шаблона и его расположения

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]

    # def get_context_data(self, **kwargs):
    #     # В первую очередь получаем базовую реализацию контекста
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Добавляем новую переменную к контексту и инициализируем её некоторым значением
    #     context['some_data'] = 'This is just some data'
    #     return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author
