from django import forms
from .models import UserProfile, SecuritySettings, NotificationSettings, PrivacySettings

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'theme', 'language']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].required = False
        self.fields['profile_picture'].label = ""

    def clean(self):
        cleaned_data = super().clean()
        profile_picture = cleaned_data.get('profile_picture')

        if not self.instance.profile_picture and 'clear_profile_picture' in self.data:
            raise forms.ValidationError("Temizlenecek bir profil fotoğrafı yok.")

        return cleaned_data

class SecuritySettingsForm(forms.ModelForm):
    class Meta:
        model = SecuritySettings
        fields = ['two_factor_auth']
        labels = {
            'two_factor_auth': 'İki Faktörlü Doğrulama',
        }

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSettings
        fields = ['issue_notifications', 'comment_notifications', 'system_notifications', 'traffic_alerts']

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = PrivacySettings
        fields = ['anonymous_reporting', 'location_access']
