from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('', views.index, name='home'),  
    path('about/', views.about, name='about'),
    path('klasat/', views.klasat_view, name='klasat'),
    path('membership/', views.membership, name='membership'),
    path('oraret/', views.oraret_view, name='oraret'),
    path('', views.index, name='index'),
]

# lejon shfaqjen e imazheve gjatë zhvillimit
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)