from django.shortcuts import render
from .forms import UserRegistrationForm, UserUpdateForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View 
from django.shortcuts import redirect
from books.models import BookData
from accounts.models import BorrowBook, UserAccount

class UserRegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('Home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('Home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('Home')
    
class UserAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        book_id = BorrowBook.objects.all()
        bookid = []
        for ids in book_id:
            bookid.append(ids.bookid)
        books = []
        for data in bookid:
            books.append(BookData.objects.filter(pk=data))

        return render(request, self.template_name, {'form': form, 'books': books})
    
    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Profile')
        return render(request, self.template_name, {'form': form})
    
def returnbook(request, id):
    book = BorrowBook.objects.filter(bookid=id).first()
    book_price = BookData.objects.filter(id=book.bookid).first().price 
    current_user = UserAccount.objects.get(user=request.user)

    current_user.balance += book_price
    current_user.save()
    book.delete()
    return redirect('Profile')
