from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from product_search import views

urlpatterns = [
    path('', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
