from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Post, Comment
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings

BAD_WORDS = [
    "badword",
    "surveillance",
    "discrimination",
    "bias",
    "autonomy",
    "accountability",
    "violations",
    "oversight",
    "safeguarding",
    "implications",
    "misuse",
]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'heading',
            'text',
            'categories',
        ]
        widgets = {
            'categories': CheckboxSelectMultiple,  # Используйте CheckboxSelectMultiple для множественного выбора
        }

    def censor(self, text):
        censor_text = []
        texte = text.split()
        for word in texte:
            if word.lower() in BAD_WORDS:  # чуточку улучшил код чтобы не было возможно обойти с помощью регистра
                censor_word = word[0] + ("*" * len(word))
                censor_text.append(censor_word)
            else:
                censor_text.append(word)

        return " ".join(censor_text)

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get('heading')
        text = cleaned_data.get('text')
        categories = cleaned_data.get('categories')
        if len(heading) < 5:
            raise ValidationError(
                "Заголовок не может быть меньше 5 символов"
            )
        if len(text) < 5:
            raise ValidationError(
                "Текст не может быть меньше 5 символов"
            )
        cleaned_data['heading'] = self.censor(heading)
        cleaned_data['text'] = self.censor(text)
        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)

        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        def censor(self, text):
            censor_text = []
            texte = text.split()
            for word in texte:
                if word.lower() in BAD_WORDS:  # чуточку улучшил код чтобы не было возможно обойти с помощью регистра
                    censor_word = word[0] + ("*" * len(word))
                    censor_text.append(censor_word)
                else:
                    censor_text.append(word)

            return " ".join(censor_text)

        def clean(self):
            cleaned_data = super().clean()
            text = cleaned_data.get('text')
            if len(text) < 5:
                raise ValidationError(
                    "Текст не может быть меньше 5 символов"
                )
            cleaned_data['text'] = self.censor(text)
            return cleaned_data
