from django import forms
from .models import Stock, ToDoItem


class ToDoItemForm(forms.ModelForm):
    creation_date = forms.DateField(label='Select Date', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ToDoItem
        fields = ['todo_id', 'title', 'content', 'creation_date', 'is_item_checked']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['creation_date'].widget.attrs.update({'class': 'special'})

    def clean_title(self):
        return self.cleaned_data['title'].strip()

    def clean_content(self):
        return self.cleaned_data['content'].strip()


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

    def clean_ticker(self):
        return self.cleaned_data['symbol'].strip()

    def clean_company_name(self):
        return self.cleaned_data['companyName'].strip()

    def clean_latest_price(self):
        return self.cleaned_data['latestPrice'].strip()

    def clean_volume(self):
        return self.cleaned_data['volume'].strip()

    def clean_market_cap(self):
        return self.cleaned_data['marketCap'].strip()

    def clean_pe_ratio(self):
        return self.cleaned_data['peRatio'].strip()

    def clean_w52_high(self):
        return self.cleaned_data['week52High'].strip()

    def clean_w52_low(self):
        return self.cleaned_data['week52Low'].strip()

    def clean_ytd_change(self):
        return self.cleaned_data['ytdChange'].strip()