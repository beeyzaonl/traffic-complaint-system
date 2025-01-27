from django.contrib import admin
from django.urls import path, include
from haritalar import views as harita_views
from django.contrib.auth import views as auth_views
from kullanicilar import views as kullanici_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', harita_views.index, name='index'),
    path('sorun/<int:sorun_id>/', harita_views.sorun_detay, name='sorun_detay'),
    path('sorun/<int:sorun_id>/oyla/', harita_views.sorun_oyla, name='sorun_oyla'),
    path('raporlar/', harita_views.raporlar, name='raporlar'),
    path('register/', kullanici_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='kullanicilar/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='kullanicilar/logout.html'), name='logout'),
    path('profil/', kullanici_views.profil, name='profil'),
    path('sorun_bildir/', harita_views.sorun_bildir, name='sorun_bildir'),
    path('', include('haritalar.urls')),  
    path('settings/', include('kullanicilar.urls')), 
]+ staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
