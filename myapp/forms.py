from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']  # Update to match your model fields
        # Optionally exclude 'author' and 'published_date' if you handle them programmatically

from .models import Researcher, Country
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth import get_user_model


# class UserAndResearcherForm(UserCreationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-color'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control custom-color'}))
#     password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control custom-color'}))
#     password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control custom-color'}))
    
#     # Researcher specific fields
#     address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-color', 'rows': 3}), required=False)
#     position_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-color'}), required=False)
#     affiliation_institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-color'}), required=False)
#     research_interests = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-color', 'rows': 4}), required=False)
#     degree_sought = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-color'}), required=False)
#     expected_degree_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control custom-color', 'type': 'date'}), required=False, help_text="Format: YYYY-MM-DD")
#     countries_of_research_focus = forms.ModelMultipleChoiceField(
#         queryset=Country.objects.all(),
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control' 'cus-color'}),
#         required=False
#     )

#     class Meta(UserCreationForm.Meta):
#         model = get_user_model()
#         fields = UserCreationForm.Meta.fields + ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control custom-color'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control custom-color'}),
#         }

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         if commit:
#             user.save()
#             researcher = Researcher(user=user)
#             # Additional researcher fields are populated here
#             researcher.save()
#             researcher.countries_of_research_focus.set(self.cleaned_data['countries_of_research_focus'])
#         return user
from django.db import transaction
User = get_user_model()
class UserAndResearcherForm(UserCreationForm):
    # Standard user fields
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-color'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control custom-color'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control custom-color'}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control custom-color'}))
    
    # Researcher specific fields
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-color', 'rows': 3}), required=False)
    position_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-color'}), required=False)
    affiliation_institution = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-color'}), required=False)
    research_interests = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-color', 'rows': 4}), required=False)
    degree_sought = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control custom-color'}), required=False)
    expected_degree_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control custom-color', 'type': 'date'}), required=False)
    country = forms.ModelMultipleChoiceField(
    queryset=Country.objects.all(),
    widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control' 'cus-color'}),
    required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control custom-color'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control custom-color'}),
        }

    def save(self, commit=True):
        with transaction.atomic():
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            if commit:
                user.save()
                
                # Assuming researcher is created for every new user registration
                researcher, created = Researcher.objects.get_or_create(user=user)
                researcher.address = self.cleaned_data.get('address', '')
                researcher.position_title = self.cleaned_data.get('position_title', '')
                researcher.affiliation_institution = self.cleaned_data.get('affiliation_institution', '')
                researcher.research_interests = self.cleaned_data.get('research_interests', '')
                researcher.degree_sought = self.cleaned_data.get('degree_sought', '')
                researcher.expected_degree_date = self.cleaned_data.get('expected_degree_date')
                
                # Saving many-to-many fields requires the instance to be saved first.
                researcher.save()
                
                # Now that the researcher instance is saved, we can set many-to-many fields.
                if 'countries_of_research_focus' in self.cleaned_data:
                    researcher.countries_of_research_focus.set(self.cleaned_data['countries_of_research_focus'])

        return user
    
from .models import ResearchItem
import datetime

class ResearchItemForm(forms.ModelForm):
    country = forms.ModelMultipleChoiceField(
    queryset=Country.objects.all(),
    widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control' 'cus-color'}),
    required=True
    )

    class Meta:
        model = ResearchItem
        fields = ['title', 'century', 'description', 'other', 'CE_or_BCE', 'author', 'published_date', 'source', 'image', 'file', 'subject', 'uploaded_by', 'country']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control custom-color'}),
            'century': forms.NumberInput(attrs={'class': 'form-control custom-color'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-color', 'rows': 4}),
            'other': forms.Textarea(attrs={'class': 'form-control custom-color', 'rows': 3}),
            'CE_or_BCE': forms.Select(attrs={'class': 'form-control custom-color'}),
            'author': forms.TextInput(attrs={'class': 'form-control custom-color'}),
            'published_date': forms.HiddenInput(),
            'source': forms.TextInput(attrs={'class': 'form-control custom-color'}),
            # Assuming 'image' and 'file' fields should also follow the same style:
            'image': forms.FileInput(attrs={'class': 'form-control custom-color'}),
            'file': forms.FileInput(attrs={'class': 'form-control custom-color'}),
            'subject': forms.TextInput(attrs={'class': 'form-control custom-color'}),
            'uploaded_by': forms.HiddenInput(),  # Hidden fields usually don't need styling
        }

    def __init__(self, *args, **kwargs):
        super(ResearchItemForm, self).__init__(*args, **kwargs)
        # Initialize the published_date with today's date if it's a new instance
        if not self.instance.pk:  # Checking if it's not a previously existing instance
            self.initial['published_date'] = datetime.date.today()


# class ResearchItemSearchForm(forms.Form):
#     query = forms.CharField(required=False, label="General Search")
#     title = forms.CharField(required=False)
#     century = forms.IntegerField(required=False)
#     description = forms.CharField(required=False)
#     other = forms.CharField(required=False)
#     CE_or_BCE = forms.ChoiceField(choices=[('', 'Any'), ('CE', 'CE'), ('BCE', 'BCE')], required=False)
#     author = forms.CharField(required=False)
#     published_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
#     source = forms.CharField(required=False)
#     country = forms.ModelChoiceField(queryset=Country.objects.all().order_by('name'), required=False, empty_label="Any")
#     subject = forms.CharField(required=False)
#     # Additional fields as needed

#     def __init__(self, *args, **kwargs):
#         super(ResearchItemSearchForm, self).__init__(*args, **kwargs)
#         self.fields['country'].queryset = Country.objects.all().order_by('name')


# class MultiSearchForm(forms.Form):
#     SEARCH_CHOICES = [
#         ('title', 'Title'),
#         ('century', 'Century'),
#         ('description', 'Description'),
#         ('author', 'Author'),
#         ('source', 'Source'),
#         ('subject', 'Subject'),
#         # Continue for other fields...
#     ]

#     search_by = forms.MultipleChoiceField(choices=SEARCH_CHOICES, widget=forms.SelectMultiple, required=False, label="Search By")
#     query = forms.CharField(required=False, label="Search Query")