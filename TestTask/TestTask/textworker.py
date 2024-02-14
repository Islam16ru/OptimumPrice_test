import re

def textnormalization(text):
    pattern = "^\s+|\n|\r|\s+$"

    outtext = ""

    if text:
        outtext = re.sub(pattern, '', text)

    return outtext