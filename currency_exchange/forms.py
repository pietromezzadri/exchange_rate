from django import forms


class QueryForm(forms.Form):
    currency_choices = [('BRL', 'Brazilian Real'),
                        ('EUR', 'Euro'), ('JPY', 'Japanese Yen')]
    currency = forms.ChoiceField(choices=currency_choices, required=True)
    initial_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    final_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True)
