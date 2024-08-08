# import inflect

# p = inflect.engine()

def pluralize(word):
    if word.endswith(('a', 'e', 'i', 'o', 'u')):
        return word + 's'
    elif word.endswith(('á', 'é', 'í', 'ó', 'ú')):
        return word[:-1] + 'es'
    elif word.endswith(('l', 'r', 'd', 'n')):
        return word + 'es'
    elif word.endswith(('z')):
        return word[:-1] + 'ces'
    else:
        return word + 's'
