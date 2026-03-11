from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Anetar, Membership, Klasa, oraret , HistoriSuksesi , Ambientet , Review
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.http import HttpResponse
from django.db.models import Q

def index(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # REVIEW
        if form_type == "review":
            emri = request.POST.get("emri")
            komenti = request.POST.get("komenti")
            rating = int(request.POST.get("rating", 5))

            if emri and komenti:
                Review.objects.create(emri=emri, komenti=komenti, rating=rating)

            return JsonResponse({
                'status': 'success',
                'msg': 'Review-i juaj u dërgua! Do aprovohet nga admini së shpejti.'
            })

        # REGJISTRIM
        elif form_type == "regjistrim":
            emri = request.POST.get("emri")
            telefoni = request.POST.get("telefoni")
            paketa = request.POST.get("paketa")

            if emri and telefoni:
                Anetar.objects.create(
                    emri=emri,
                    telefoni=telefoni,
                    paketa=paketa,
                    burimi="Regjistrim Pakete"
                )

            return JsonResponse({
                'status': 'success',
                'msg': 'Regjistrimi u krye me sukses! Do ju kontaktojmë së shpejti.'
            })

        return JsonResponse({'status': 'error'})

    reviews = Review.objects.filter(approved=True).order_by("-data")
    historite = HistoriSuksesi.objects.all()[:3]

    for review in reviews:
        val = int(review.rating)
        review.stars = range(val)
        review.empty_stars = range(5 - val)

    return render(request, "index.html", {
        "reviews": reviews,
        "historite": historite
    })


# Dashboard
def dashboard_view(request):
    lista_orareve = oraret.objects.all().order_by('ora_fillimit')
    tabela_orareve = krijo_tabelen(lista_orareve)  
    context = {
        'anetaret': Anetar.objects.all(),
        'reviews': Review.objects.all(),
        'klasat': Klasa.objects.all(),
        'historite': HistoriSuksesi.objects.all(),
        'ambientet': Ambientet.objects.all(),
        'tabela_orareve': tabela_orareve, 
    }
    return render(request, 'dashboard.html', context)  



def krijo_tabelen(oraret_queryset):
    tabela = defaultdict(lambda: defaultdict(str))
    for orar in oraret_queryset:
        ora = f"{orar.ora_fillimit} - {orar.ora_mbarimit}"
        dita = orar.dita
        tabela[ora][dita] = f"{orar.klasa} ({orar.salla})"
        
    return dict(tabela)


def about(request):
    if request.method == "POST":
        emri = request.POST.get("emri")
        telefoni = request.POST.get("telefoni")
        paketa = request.POST.get("paketa")
        if emri and telefoni:
            Anetar.objects.create(
                emri=emri,
                telefoni=telefoni,
                paketa=paketa,
                burimi="Regjistrim Pakete"
            )
        return JsonResponse({'status': 'success', 'msg': f'Faleminderit {emri}! Do ju kontaktojmë së shpejti.'})

    historite = HistoriSuksesi.objects.all()
    ambientet = Ambientet.objects.all()
    return render(request, 'about.html', {
        'historite': historite,
        'ambientet': ambientet
    })


def klasat_view(request):
    if request.method == "POST":
        emri = request.POST.get("emri")
        telefoni = request.POST.get("telefoni")
        paketa = request.POST.get("paketa")
        if emri and telefoni:
            Anetar.objects.create(
                emri=emri,
                telefoni=telefoni,
                paketa=paketa,
                burimi="Regjistrim Pakete"
            )
        return JsonResponse({'status': 'success', 'msg': f'Faleminderit {emri}! Do ju kontaktojmë së shpejti.'})

    all_klasat = Klasa.objects.all()

    for k in all_klasat:
        if k.pikat_e_klases:
            k.pikat_e_klases_list = k.pikat_e_klases.split("\n")
        else:
            k.pikat_e_klases_list = []

    return render(request, 'Klasat.html', {'all_klasat': all_klasat})


def oraret_view(request):
    ditet_db = ["E_HËNË", "E_MARTË", "E_MËRKURË", "E_ENJTE", "E_PREMTE", "E_SHTUNË"]
    ditet_display = ["E HËNË", "E MARTË", "E MËRKURË", "E ENJTE", "E PREMTE", "E SHTUNË"]

    emrat_e_sallave = ["1", "2"]

    tabela_per_sallat = {}

    for salla in emrat_e_sallave:
        kohet = oraret.objects.filter(salla=salla).values('ora_fillimit', 'ora_mbarimit').distinct().order_by('ora_fillimit')

        lista_rreshtave = []
        for k in kohet:
            ora_str = f"{k['ora_fillimit'].strftime('%H:%M')} - {k['ora_mbarimit'].strftime('%H:%M')}"
            rreshti = {'ora': ora_str, 'klasat': []}

            for dita in ditet_db:
                klasa = oraret.objects.filter(salla=salla, ora_fillimit=k['ora_fillimit'], dita=dita).first()
                rreshti['klasat'].append(klasa.klasa if klasa else "")
            lista_rreshtave.append(rreshti)

        tabela_per_sallat[f"Salla {salla}"] = lista_rreshtave

    return render(request, 'oraret.html', {
        'tabela_per_sallat': tabela_per_sallat,
        'ditet_display': ditet_display
    })


def histori_suksesi(request):
    historite = HistoriSuksesi.objects.all()
    return render(request, 'histori_suksesi.html', {'historite': historite})


def membership(request):
    all_memberships = Membership.objects.all()
    return render(request, 'membership.html', {"all_memberships": all_memberships})


def FrontPage(request):
    return render(request, 'index.html')


# Formular kontakti
def kontakt(request):
    if request.method == "POST":
        emri = request.POST.get('emri')
        telefoni = request.POST.get('telefoni')
        email = request.POST.get('email')
        paketa = request.POST.get('paketa')
        mesazhi = request.POST.get('mesazhi')

        if paketa and telefoni:
            Anetar.objects.create(
                emri=emri,
                telefoni=telefoni,
                paketa=paketa,
                burimi="Regjistrim Pakete"
            )
            return JsonResponse({
                'status': 'success',
                'msg': 'Regjistrimi u krye me sukses! Do ju kontaktojmë së shpejti.'
            })

        elif email and mesazhi:
            Anetar.objects.create(
                emri=emri,
                email=email,
                mesazhi=mesazhi,
                burimi="Kontakt nga Footeri"
            )
            return JsonResponse({
                'status': 'success',
                'msg': 'Mesazhi u dërgua me sukses! Do ju përgjigjemi së shpejti.'
            })

        # FIX: explicit error if neither condition matched on POST
        return JsonResponse({'status': 'error', 'msg': 'Të dhënat janë të pakompletuara.'})

    return JsonResponse({'status': 'error', 'msg': 'Metoda e kërkesës nuk është e vlefshme.'})

