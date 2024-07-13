from .models import Post
from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=250)
    text = forms.Textarea()


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            "title",
            "image",
            "content",
            "category",
            "published_date",
        )
