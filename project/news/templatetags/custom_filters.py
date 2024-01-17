from django import template

register = template.Library()

BAD_WORDS = [
     "BADWORD"
]


@register.filter()
def censor(text):
    censor_text = []
    texte = text.split()
    for word in texte:
        if word.upper() in BAD_WORDS:  # чуточку улучшил код чтобы не было возможно обойти с помощью регистра
            censor_word = word[0] + ("*" * len(word))
            censor_text.append(censor_word)
        else:
            censor_text.append(word)

    return " ".join(censor_text)
