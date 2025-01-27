from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Profil, UserProfile, SecuritySettings, NotificationSettings, PrivacySettings
from .forms import UserProfileForm, SecuritySettingsForm, NotificationSettingsForm, PrivacySettingsForm
from django.contrib import messages

def settings(request):
    return render(request, 'kullanicilar/settings/settings.html')

@login_required
def account_settings(request):
    if request.method == 'POST':
        if not hasattr(request.user, 'userprofile'):
            UserProfile.objects.create(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            if 'clear_profile_picture' in request.POST:
                try:
                    request.user.userprofile.profile_picture.delete()
                    messages.success(request, 'Profil fotoğrafı kaldırıldı.')
                except ValueError:  
                    messages.error(request, 'Temizlenecek bir profil fotoğrafı yok.')
            else:
                form.save()
                messages.success(request, 'Ayarlar kaydedildi.')
                return redirect('account_settings')
            return redirect('settings')
    else:
        if not hasattr(request.user, 'userprofile'):
            UserProfile.objects.create(user=request.user)
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'kullanicilar/settings/account_settings.html', {'form': form})

def security_settings(request):

    if not hasattr(request.user, 'securitysettings'):
        SecuritySettings.objects.create(user=request.user)

    if request.method == 'POST':
        form = SecuritySettingsForm(request.POST, instance=request.user.securitysettings)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            messages.success(request, 'Güvenlik ayarları başarıyla güncellendi.')
            return redirect('settings')
    else:
        form = SecuritySettingsForm(instance=request.user.securitysettings)

    return render(request, 'kullanicilar/settings/security_settings.html', {'form': form})

def notification_settings(request):
    if request.method == 'POST':
        if not hasattr(request.user, 'notificationsettings'):
            NotificationSettings.objects.create(user=request.user)
        form = NotificationSettingsForm(request.POST, instance=request.user.notificationsettings)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        if not hasattr(request.user, 'notificationsettings'):
            NotificationSettings.objects.create(user=request.user)
        form = NotificationSettingsForm(instance=request.user.notificationsettings)
    return render(request, 'kullanicilar/settings/notification_settings.html', {'form': form})

def privacy_settings(request):
    if request.method == 'POST':
        if not hasattr(request.user, 'privacysettings'):
            PrivacySettings.objects.create(user=request.user)
        form = PrivacySettingsForm(request.POST, instance=request.user.privacysettings)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        if not hasattr(request.user, 'privacysettings'):
            PrivacySettings.objects.create(user=request.user)
        form = PrivacySettingsForm(instance=request.user.privacysettings)
    return render(request, 'kullanicilar/settings/privacy_settings.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hesabınız başarıyla oluşturuldu! Giriş yapabilirsiniz.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")  
    else:
        form = UserCreationForm()
    return render(request, 'kullanicilar/register.html', {'form': form})

@login_required
def profil(request):
    profil = get_object_or_404(Profil, kullanici=request.user)
    sorunlar = profil.kullanici.trafiksorunu_set.all()
    yorumlar = profil.kullanici.yorum_set.all()
    context = {
        'profil': profil,
        'sorunlar': sorunlar,
        'yorumlar': yorumlar,
    }
    return render(request, 'kullanicilar/profil.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  
    else:
        form = AuthenticationForm()
    return render(request, 'kullanicilar/login.html', {'form': form})