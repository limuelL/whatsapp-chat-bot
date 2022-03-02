from googletrans import Translator

translator = Translator()


def translate(message):

    translation = translator.translate(message)
    translated_text = translation.text

    return translated_text
