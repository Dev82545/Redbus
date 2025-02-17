from django import forms
from .models import passengers
from redbus.models import Seat_booked

class SeatBookedForm(forms.ModelForm):
    class Meta:
        model = Seat_booked
        fields = ['buses', 'passengers']
        widgets = {
            'passengers': forms.CheckboxSelectMultiple(),  # or any widget you prefer
        }
        
    def clean(self):
        cleaned_data = super().clean()
        tseat_number = cleaned_data.get('tseat_number')
        passengers = cleaned_data.get('passengers')

        # Note: 'passengers' may be a QuerySet, so we can get its length.
        if tseat_number is not None and passengers is not None:
            if tseat_number != passengers.count():
                raise forms.ValidationError(
                    "The number of passengers selected must match the number of seats booked."
                )
        return cleaned_data

class PassengerForm(forms.ModelForm):
    class Meta:
        model = passengers
        fields = ['name', 'age', 'gender']


class WalletTopUpForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    
class SelectPassengersForm(forms.Form):
    # The field will list only the passengers belonging to the current user.
    # We leave the queryset empty initially and set it in the view.
    passengers = forms.ModelMultipleChoiceField(
        queryset=passengers.objects.none(),
        widget=forms.CheckboxSelectMultiple,  # or any widget you prefer
        required=False,
        label="Select Saved Passengers"
    )
