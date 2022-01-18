from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import ngettext_lazy


class MinWordsValidator(MinLengthValidator):
    """
        Sub-class of the MinLengthValidator to check if row includes enough words.
    """

    code = 'min_words'

    message = ngettext_lazy(
        'Ensure this value has at least %(limit_value)d word (it has %(show_value)d).',
        'Ensure this value has at least %(limit_value)d words (it has %(show_value)d).',
        'limit_value')

    def compare(self, a, b):
        return a <= b.split()


class MinSentencesValidator(MinLengthValidator):
    """
        Sub-class of the MinLengthValidator to check if row includes enough sentences.
    """

    code = 'min_sentences'

    message = ngettext_lazy(
        'Ensure this value has at least %(limit_value)d sentence (it has %(show_value)d).',
        'Ensure this value has at least %(limit_value)d sentences (it has %(show_value)d).',
        'limit_value')

    def compare(self, a, b):
        return a <= b.split('.')


class MaxSentenceValidator(MaxLengthValidator):
    """
        Sub-class of the MinLengthValidator to check if amount of sentences less than limit.
    """

    message = ngettext_lazy(
        'Ensure this value has at most %(limit_value)d sentence (it has %(show_value)d).',
        'Ensure this value has at most %(limit_value)d sentences (it has %(show_value)d).',
        'limit_value')
    code = 'max_length'

    def compare(self, a, b):
        return a >= b.split('.')


