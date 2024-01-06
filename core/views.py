from django.shortcuts import render
from django.views.generic import TemplateView
from books.models import BookData
from categories.models import Category

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cat_slug = self.kwargs.get('cat_slug')
        books = BookData.objects.all()
        if cat_slug is not None:
            category = Category.objects.get(slug=cat_slug)
            books = BookData.objects.filter(category=category)


        categories = Category.objects.all()

        context['books'] = books 
        context['categories'] = categories
        return context

