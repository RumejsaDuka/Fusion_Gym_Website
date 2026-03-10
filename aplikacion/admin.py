from django.contrib import admin
from .models import Anetar, Membership, Klasa, oraret, HistoriSuksesi, Ambientet, Review

# 1. Konfigurimi për Anetarët
class AnetarAdmin(admin.ModelAdmin):
    list_display = ('emri', 'telefoni', 'email', 'paketa', 'shfaq_mesazhin', 'burimi', 'data_regjistrimit')
    search_fields = ('emri', 'email', 'telefoni')
    list_filter = ('paketa', 'burimi', 'data_regjistrimit')

    def shfaq_mesazhin(self, obj):
        return obj.mesazhi[:30] + "..." if obj.mesazhi else "-"
    shfaq_mesazhin.short_description = 'Mesazhi'

# 2. Konfigurimi për Reviews (Kujdes emrin: ReviewAdmin)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('emri', 'rating', 'approved', 'data', 'shfaq_komentin')
    list_editable = ('approved',)
    list_filter = ('approved', 'rating', 'data')
    search_fields = ('emri', 'komenti')

    def shfaq_komentin(self, obj):
        return obj.komenti[:50] + "..." if obj.komenti else "-"
    shfaq_komentin.short_description = 'Komenti'

# Emërtoje klasën Admin në mënyrë që të jetë e qartë se cilin model po stilon
class MembershipAdmin(admin.ModelAdmin):
    # Emrat e fushave duhet të jenë fiks si te models.py (zakonisht me shkronja të vogla)
    list_display = ('title', 'price', 'duration_months') 
    
    # Kjo lejon kërkimin sipas emrit të paketës
    search_fields = ('title',) 
    
    # Lejon ndryshimin e çmimit direkt nga tabela
    list_editable = ('price',)

# Oraret
class OraretAdmin(admin.ModelAdmin):
    # Kolonat që do të shfaqen në tabelë
    list_display = ('klasa', 'dita', 'ora_fillimit', 'ora_mbarimit', 'salla')
    
    # Filtra anash për të gjetur oraret sipas ditës ose klasës
    list_filter = ('dita', 'klasa', 'salla')
    
    # Kërkimi për klasën ose sallën
    search_fields = ('klasa', 'salla')
    
    # Renditja automatike sipas ditës dhe orës së fillimit
    ordering = ('dita', 'ora_fillimit')

# Klasat Admin
class KlasatAdmin(admin.ModelAdmin):
    # Kujdes: Emrat duhet të jenë EKZAKTËSISHT si në model (pa hapësira anash)
    list_display = ("titulli", "shfaq_pershkrimin_shkurter", "ka_imazh")
    search_fields = ("titulli",)

    def shfaq_pershkrimin_shkurter(self, obj):
        # Përdorim [:50] për të marrë 50 karakteret e para
        if obj.pershkrim_i_shkurter:
            return obj.pershkrim_i_shkurter[:50] + "..."
        return "-"
    shfaq_pershkrimin_shkurter.short_description = "Përshkrimi"
    
    def ka_imazh(self, obj):
        return bool(obj.imazhi)
    ka_imazh.boolean = True
    ka_imazh.short_description = 'Imazhi'


# historiku i suksesit 
class HistoriSuksesiAdmin(admin.ModelAdmin):
    # Shfaqim emrin, një pjesë të përshkrimit dhe datën
    list_display = ('emri', 'shfaq_pershkrimin', 'data_krijimit')
    search_fields = ('emri',)
    list_filter = ('data_krijimit',)

    def shfaq_pershkrimin(self, obj):
        return obj.pershkrimi_shkurter[:50] + "..." if obj.pershkrimi_shkurter else "-"
    shfaq_pershkrimin.short_description = "Përmbledhje"

# ambientet
class AmbientetAdmin(admin.ModelAdmin):
    list_display = ('pershkrim', 'ka_foto')
    search_fields = ('pershkrim',)

    def ka_foto(self, obj):
        return bool(obj.foto)
    ka_foto.boolean = True
    ka_foto.short_description = 'Statusi i Fotos'



# 3. Regjistrimi i Modeleve (VETËM NJË HERË PËR ÇDO MODEL)
admin.site.register(Anetar, AnetarAdmin)
admin.site.register(Review, ReviewAdmin) # Këtu i lidhim të dyja bashkë
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Klasa, KlasatAdmin)
admin.site.register(oraret, OraretAdmin)
admin.site.register(HistoriSuksesi, HistoriSuksesiAdmin)
admin.site.register(Ambientet, AmbientetAdmin)
