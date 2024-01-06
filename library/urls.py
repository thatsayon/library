from django.contrib import admin
from django.urls import path, include
from core.views import HomeView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view(), name="Home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('book/', include('books.urls')),
    path('transactions/', include('transactions.urls')),
    path('category/<slug:cat_slug>/', HomeView.as_view(), name="CatSlug"),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)