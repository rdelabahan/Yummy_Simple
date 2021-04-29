from django import forms
from ckeditor.fields import RichTextFormField

class RecipeForm(forms.Form):

    title = forms.CharField(label = 'Recipe Title', min_length = 2, max_length = 50, widget = forms.TextInput(attrs = {'id':'title'}))
    content = RichTextFormField(label = False, widget = forms.Textarea(attrs={'id':'editor1'}))
    
    
