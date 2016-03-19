from django import forms

class SearchForm(forms.Form) :
    search_string = forms.CharField(label = 'Search String' , max_length=100 , widget = forms.TextInput(attrs = {'class' : 'some_class'}))
    show_count = forms.BooleanField()
