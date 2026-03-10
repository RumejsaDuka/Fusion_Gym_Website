from django.db import models
import datetime

class Anetar(models.Model):
    emri = models.CharField(max_length=100) 
    telefoni = models.CharField(max_length=20, null=True, blank=True) # E bëjmë opsionale
    email = models.EmailField(null=True, blank=True) # Shtohet për footerin
    paketa = models.CharField(max_length=50, null=True, blank=True)
    mesazhi = models.TextField(null=True, blank=True) # Shtohet për footerin
    data_regjistrimit = models.DateTimeField(auto_now_add=True)

    # Një fushë ndihmëse për ta parë në Dashboard nga erdhi kërkesa
    burimi = models.CharField(max_length=50, default="Paketa") 

    def __str__(self):
        return f"{self.emri} - {self.burimi}"
    
    class Meta:
        verbose_name = "Regjistrime"
        verbose_name_plural = "Regjistrimet"
    

class Membership(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.TextField()
    duration_months = models.IntegerField(default=1)
    e_rekomanduar = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Paketa"
        verbose_name_plural = "Paketat"
    

class Klasa(models.Model):
    titulli = models.CharField(max_length=100)
    pershkrim_i_shkurter = models.CharField(max_length=250)
    pershkrim_i_detajuar = models.TextField(blank=True, null=True)
    pikat_e_klases = models.TextField(help_text="Shkruaj pikat e ndara me Enter")
    # Fushat e reja:
    target_group = models.CharField(max_length=100, default="Gjithësecili", help_text="P.sh. Fillestarë, Sportistë Elite, etj.")
    intensiteti = models.CharField(max_length=50, default="I Lartë")
    kohezgjatja = models.IntegerField(default=60) # Kohëzgjatja në minuta
    
    imazhi = models.ImageField(upload_to='klasat/')

    def __str__(self):
        return self.titulli

    class Meta:
        verbose_name = "Klasa"
        verbose_name_plural = "Klasat"

    def lista_e_pikave(self):
        if self.pikat_e_klases:
            return self.pikat_e_klases.splitlines()
        return []

class oraret(models.Model):
    DAYS = [
        ("E_HËNË", "E HËNË"),
        ("E_MARTË", "E MARTË"),
        ("E_MËRKURË", "E MËRKURË"),
        ("E_ENJTE", "E ENJTE"),
        ("E_PREMTE", "E PREMTE"),
        ("E_SHTUNË", "E SHTUNË"),
    ]

    salla = models.CharField(max_length=20)
    dita = models.CharField(max_length=20, choices=DAYS)
    ora_fillimit = models.TimeField(default=datetime.time(8, 0))
    ora_mbarimit = models.TimeField(default=datetime.time(16, 0))
    klasa = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "oraret"

    def __str__(self):
        return f"{self.salla} - {self.dita} - {self.ora_fillimit} - {self.ora_mbarimit} - {self.klasa}"
    

class HistoriSuksesi(models.Model):
    emri=models.CharField(max_length=30)
    pershkrimi_shkurter = models.CharField(max_length=200)
    foto_para = models.ImageField(upload_to='transformime/')
    foto_pas = models.ImageField(upload_to='transformime/')
    data_krijimit = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foto Para/Pas"
        verbose_name_plural = "Foto Para/Pas"

    def __str__(self):
        return self.emri 
    
class Ambientet(models.Model):
    foto = models.ImageField(upload_to='ambient/')
    pershkrim = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Ambientet'

    def __str__(self):
        return self.pershkrim
    
class Review(models.Model):
    emri = models.CharField(max_length=100)
    komenti = models.TextField()
    rating = models.IntegerField(default=5)
    approved = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.emri