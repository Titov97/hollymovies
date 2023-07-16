import re
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_comma_separated_integer_list

from viewer.models import Genre, Movie, User, Profile


class PastMonthField(forms.DateField):

    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Only past dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=1)


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError("Scrie ba cu LITERA MARE")


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

    # title_form = forms.CharField(max_length=128, validators=[capitalized_validator])
    # genre_form = forms.ModelChoiceField(queryset=Genre.objects.all())
    # rating_form = forms.IntegerField(min_value=1, max_value=10)
    # released_form = PastMonthField()
    # description_form = forms.CharField(widget=forms.Textarea, required=False)

    def clean_description_form(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description_form']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def clean(self):
        result = super().clean()
        if result['genre_form'].name == 'Comedy' and result['rating_form'] > 5:
            raise ValidationError('Comedy aren`t so good')
        return result


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'date_of_birth')

    biography = forms.CharField()

    def save(self, commit=True):
        result = super().save(commit=commit)
        if commit:
            bio = self.cleaned_data['biography']
            profile = Profile.objects.create(user=result, biography=bio)

        return result
