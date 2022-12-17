from django.contrib.auth.decorators import permission_required

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
import datetime
from django.urls import reverse

from .models import Book, Genre, BookInstance, Author
from .forms import RenewBookModelForm

from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request,
                  'index.html',
                  context={
                      'num_books': num_books,
                      'num_instances': num_instances,
                      'num_instances_available': num_instances_available,
                      'num_authors': num_authors,
                      'num_genres': num_genres,
                      'num_matches_books': num_matches_books,
                      'num_visits': num_visits, }, )


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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    :param request:
    :param pk:
    :return:
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding)
        form = RenewBookModelForm(request.POST)

        # Проверка валидности данных формы
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            # (здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form
            book_inst.save()

            # Переход по адресу 'all-borrowed'
            return HttpResponseRedirect(reverse('all-borrowed'))

    # Если это GET или какой-либо еще (первое обращение к форме), создать форму по умолчанию
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016', }


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
