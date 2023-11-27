from django import forms
from .models import Post, Reply
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        category_choices = kwargs.pop('category_choices', None)
        super().__init__(*args, **kwargs)
        if category_choices:
            self.fields['category'].queryset = category_choices

    image = forms.ImageField(required=False)
    video_url = forms.URLField(required=False)

    class Meta:
        model = Post
        fields = ['category', 'post_title', 'post_text', 'image', 'video_url']

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("post_text")
        if description is not None and len(description) < 5:
            raise ValidationError({
                "description": "Описание не может быть менее 5 символов."
            })

        name = cleaned_data.get("post_title")
        if name == description:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            'reply_text',
        ]