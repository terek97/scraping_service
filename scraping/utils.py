from transliterate import translit
from transliterate import detect_language


def make_slug(text):
    text = text.replace(' ', '_').lower()
    if detect_language(text) == 'ru':
        return translit(text, reversed=True)
    else:
        return text

