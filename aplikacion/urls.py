from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('about/', views.about, name='about'),
#     path('klasat/', views.klasat_view, name='klasat'),
#     path('membership/', views.membership, name='membership'),
#     path('footer/', views.kontakt, name='kontakt'),
#     # path('lista-anetareve/', views.lista_anetareve, name='lista_anetareve'),
#     path('FrontPage/', views.FrontPage, name='FrontPage'),
#     path('histori_suksesi/', views.histori_suksesi, name='histori_suksesi'),
# ]


urlpatterns = [
    path('', views.index, name='home'),  # Shto name='home' këtu
    path('about/', views.about, name='about'),
    path('klasat/', views.klasat_view, name='klasat'),
    path('membership/', views.membership, name='membership'),
    path('oraret/', views.oraret_view, name='oraret'),
    path('', views.index, name='index'),
]

# Kjo lejon shfaqjen e imazheve gjatë zhvillimit
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)