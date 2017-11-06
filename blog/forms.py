from django import forms
from .models import Comment,Article,Profile
from django.contrib.auth.models import User 
from ckeditor.widgets import CKEditorWidget
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="password2",widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ('username','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title','content','draft','tags')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone','sex','avatar')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email')