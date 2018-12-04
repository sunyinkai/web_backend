from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)


class PostForm(forms.Form):
    body = forms.CharField(label="What do you think?", max_length=100)


class CommentForm(forms.Form):
    body = forms.CharField(label='what are what to comment?', max_length=100)
