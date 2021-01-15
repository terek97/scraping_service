from transliterate import translit


def make_slug(text):
    text = text.replace(' ', '_').lower()
    return translit(text, reversed=True)

