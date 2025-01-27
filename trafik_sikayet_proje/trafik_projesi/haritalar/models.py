from django.db import models
from django.contrib.auth.models import User

class TrafikSorunu(models.Model):
    konum = models.CharField(max_length=255)
    KATEGORI_SECENEKLERI = (
        ('Yol Çalışması', 'Yol Çalışması'),
        ('Trafik Kazası', 'Trafik Kazası'),
        ('Radar', 'Radar'),
        ('Sel Baskını', 'Sel Baskını'),
        ('Heyelan', 'Heyelan'),
        ('Trafik Lambası Arızası', 'Trafik Lambası Arızası'),
        ('Yolda Çökme', 'Yolda Çökme'),
        ('Vahşi Hayvan Çıkabilir', 'Vahşi Hayvan Çıkabilir'),
    )
    kategori = models.CharField(max_length=255, choices=KATEGORI_SECENEKLERI)
    aciklama = models.TextField(blank=True)
    tarih = models.DateTimeField(auto_now_add=True)
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    oylar = models.IntegerField(default=0)
    puan = models.IntegerField(default=0)
    oy_verenler = models.ManyToManyField(User, related_name='oy_verilen_sorunlar', blank=True)
    gorsel = models.ImageField(upload_to='sorun_gorselleri/', blank=True, null=True)  

    def __str__(self):
        return f"{self.kategori} - {self.konum}"


class Yorum(models.Model):
    sorun = models.ForeignKey(TrafikSorunu, on_delete=models.CASCADE, related_name='yorumlar')
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    icerik = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)
    puan = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.kullanici.username} - {self.sorun}"
