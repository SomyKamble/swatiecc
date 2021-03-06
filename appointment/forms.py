from django import forms
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ('patient', 'symptoms', 'prescription')

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['patient'].queryset = User.objects.filter(user_type="P")


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['patient'].queryset = User.objects.filter(user_type="P")
            self.fields['doctor'].queryset = User.objects.filter(user_type="D")
            self.fields["date"].label = "Date (YYYY-MM-DD)"
            self.fields["time"].label = "Time 24 hr (HH:MM)"
        


from . models import Encfile

class upload_form(forms.ModelForm):
    class Meta:
        model = Encfile
        fields = ('to_user','file',)



class intake(forms.Form):
    public_key = forms.CharField(label="public key")
    file = forms.FileField(label="file")


class Key_create(forms.ModelForm):
    class Meta:
        model = Keys
        fields = ('private_key','public_key',)