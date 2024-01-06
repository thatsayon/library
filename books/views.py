from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import BookData
from accounts.models import UserAccount, BorrowBook
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .forms import ReviewForm

def send_transaction_email(user, bookn, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'book' : bookn,
            'amount': amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class BookDetailView(DetailView):
    model = BookData
    pk_url_kwarg = 'id'
    template_name = 'detail.html'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()

        

        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book 
            new_review.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        reviews = book.review.all()
        review_form = ReviewForm()

        context['book'] = book
        context['reviews'] = reviews
        book_id = self.kwargs.get('id')
        context['show_review_form'] = False
        if BorrowBook.objects.filter(bookid=book_id):
            context['show_review_form'] = True

        context['review_form'] = review_form
        return context


def borrowbook(request, id):
    book = BookData.objects.filter(pk=id).first()
    print(book.price)
    current_user = UserAccount.objects.get(user=request.user)

    if current_user.balance < book.price:
        messages.error(
            request,
            f'You need more ${book.price - current_user.balance}'
        )
        return redirect("BookD", id=id)

    if BorrowBook.objects.filter(bookid=id):
        messages.error(
            request,
            f'You already borrow this book.'
        )
        return redirect("BookD", id=id)
    else:
        BorrowBook.objects.create(
            user=current_user,
            bookid=id
        )
        current_user.balance = current_user.balance - book.price
        current_user.save()
        send_transaction_email(request.user, book.title, book.price, "Borrow Book", "borrow.html")
        return redirect("BookD", id=id)

    return redirect("BookD", id=id)
