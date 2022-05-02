from django import forms
from django.contrib.auth import get_user_model
from .models import Vote, Movie
from django.forms import ModelForm, TextInput, DateInput


class VoteForm(forms.ModelForm):
    movie = forms.ModelChoiceField(widget=forms.HiddenInput,queryset=Movie.objects.all(),
        disabled=True)
    value = forms.IntegerField()

    class Meta:
        model = Vote
        fields = ("value","movie")

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'year', 'preview', 'rating', 'runtime', 'plot']
        widgets = {'title': TextInput(attrs={'class': 'form-input'}),
                   'genre': TextInput(attrs={'class': 'form-input'}),
                   'preview': forms.Textarea(attrs={'cols': 100, 'rows': 30}),
                   'year': forms.DateInput(attrs={'class': 'form-control'})}

