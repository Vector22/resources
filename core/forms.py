from django import forms

from core.models import Reservation


class ReservationModelForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        localize=True,
        widget=forms.DateTimeInput(format='%d/%m/%Y',
                                   attrs={'type': 'datetime-local'}),
    )
    end_date = forms.DateTimeField(
        localize=True,
        widget=forms.DateTimeInput(format='%d/%m/%Y',
                                   attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = Reservation
        fields = [
            'title',
            'overview',
            'start_date',
            'end_date',
        ]

    # Here we override the form elements attributes to add boostrap class
    def __init__(self, *args, **kwargs):
        super(ReservationModelForm, self).__init__(*args, **kwargs)
        # Add some attributes for bootstrap
        self.fields['title'].widget.attrs[
            'placeholder'] = 'Title of reservation'
        self.fields['title'].widget.attrs['name'] = 'title'
        self.fields['overview'].widget.attrs['rows'] = '1'
        self.fields['overview'].widget.attrs['placeholder'] = 'Small overview'
        self.fields['overview'].widget.attrs['name'] = 'overview'
        self.fields['start_date'].widget.attrs['name'] = 'start_date'
        self.fields['end_date'].widget.attrs['name'] = 'end_date'

        # add the same class to all the fields (commom attribute value for all)
        for field in self.fields:
            self.fields[field].widget.attrs[
                'class'] = 'form-control form-control-lg'
