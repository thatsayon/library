from django.urls import path 
from .views import BookDetailView, borrowbook

urlpatterns = [
    path('detail/<int:id>/', BookDetailView.as_view(), name="BookD"),
    path('borrow/<int:id>/', borrowbook, name="Borrow"),
]
