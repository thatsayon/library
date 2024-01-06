from django.db import models
from categories.models import Category

class BookData(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='books/media/uploads')
    price = models.DecimalField(decimal_places=2, max_digits=7)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

class Reviews(models.Model):
    book = models.ForeignKey(BookData, on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comments by {self.name}"