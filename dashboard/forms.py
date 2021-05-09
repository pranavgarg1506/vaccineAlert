from django import forms

class SearchForm(forms.Form):

    pincode = forms.CharField( label = 'Pin Code', required = True)
    date = forms.DateField( label = 'Query Date', widget = forms.SelectDateWidget)

    email = forms.EmailField(label = 'Email')