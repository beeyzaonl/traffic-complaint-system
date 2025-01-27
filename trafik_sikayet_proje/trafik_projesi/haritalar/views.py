from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TrafikSorunu, Yorum
from kullanicilar.models import Profil
from .forms import TrafikSorunuForm, YorumForm, SorunFiltreForm
from django.db.models import Count
from django.contrib import messages

def index(request):
    sorunlar = TrafikSorunu.objects.all().order_by('-tarih')  
    return render(request, 'haritalar/index.html', {'sorunlar': sorunlar})

@login_required
def sorun_bildir(request):
    if request.method == 'POST':
       form = TrafikSorunuForm(request.POST, request.FILES)  
       if form.is_valid():
            sorun = form.save(commit=False)
            sorun.kullanici = request.user
            sorun.save()

            messages.success(request, 'Sorun başarıyla bildirildi.')

            profil = request.user.profil
            profil.puan += 10
            profil.save()

            return redirect('index')
    else:
        form = TrafikSorunuForm()
    return render(request, 'haritalar/sorun_bildir.html', {'form': form})

def sorun_detay(request, sorun_id):
    sorun = get_object_or_404(TrafikSorunu, pk=sorun_id)
    yorumlar = Yorum.objects.filter(sorun=sorun)
    if request.method == 'POST':
        form = YorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.kullanici = request.user
            yorum.sorun = sorun
            yorum.save()
            messages.success(request, 'Yorumunuz başarıyla eklendi.')

            profil = request.user.profil
            profil.puan += 5
            profil.save()

            return redirect('sorun_detay', sorun_id=sorun.id)
    else:
        form = YorumForm()
    return render(request, 'haritalar/sorun_detay.html', {'sorun': sorun, 'yorumlar': yorumlar, 'form': form})

@login_required
def sorun_oyla(request, sorun_id):
    sorun = get_object_or_404(TrafikSorunu, pk=sorun_id)
    if request.user in sorun.oy_verenler.all(): 
        messages.error(request, 'Bu soruna zaten oy verdiniz.')
    else:
        sorun.oylar += 1
        sorun.oy_verenler.add(request.user)  
        sorun.save()
        messages.success(request, 'Oyunuz kaydedildi.')

    profil = request.user.profil
    profil.puan += 1
    profil.save()

    return redirect('sorun_detay', sorun_id=sorun.id)

@login_required  
def raporlar(request):
    sorunlar = TrafikSorunu.objects.all()
    filtre_form = SorunFiltreForm(request.GET)

    if filtre_form.is_valid():
        kategori = filtre_form.cleaned_data.get('kategori')
        baslangic_tarihi = filtre_form.cleaned_data.get('baslangic_tarihi')
        bitis_tarihi = filtre_form.cleaned_data.get('bitis_tarihi')
        konum = filtre_form.cleaned_data.get('konum')

        if kategori:
            sorunlar = sorunlar.filter(kategori=kategori)
        if baslangic_tarihi:
            sorunlar = sorunlar.filter(tarih__gte=baslangic_tarihi)
        if bitis_tarihi:
            sorunlar = sorunlar.filter(tarih__lte=bitis_tarihi)
        if konum:
            sorunlar = sorunlar.filter(konum__icontains=konum)

    kategori_dagilimi = sorunlar.values('kategori').annotate(sorun_sayisi=Count('id'))
    labels = [item['kategori'] for item in kategori_dagilimi]
    data = [item['sorun_sayisi'] for item in kategori_dagilimi]

    context = {
        'labels': labels,
        'data': data,
        'sorunlar': sorunlar,
        'filtre_form': filtre_form
    }
    return render(request, 'haritalar/raporlar.html', context)