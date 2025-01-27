from django import forms
from .models import TrafikSorunu, Yorum

class TrafikSorunuForm(forms.ModelForm):
    konum = forms.CharField(widget=forms.TextInput(attrs={'id': 'konum'}))
    

    class Meta:
        model = TrafikSorunu
        fields = ['konum', 'kategori', 'aciklama','gorsel']

class YorumForm(forms.ModelForm):
    class Meta:
        model = Yorum
        fields = ['icerik']

class SorunFiltreForm(forms.Form):
    kategori = forms.ChoiceField(choices=[(kategori, kategori) for kategori in TrafikSorunu.objects.values_list('kategori', flat=True).distinct()], required=False)
    baslangic_tarihi = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    bitis_tarihi = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    konum = forms.CharField(max_length=200, required=False)