import string
def punctuation_remover(text):
    BENGALI_PUNCTUATION = string.punctuation + " —।’‘"
    BENGALI_NUMERALS = "০১২৩৪৫৬৭৮৯"
    return text.translate(str.maketrans(' ', ' ', BENGALI_PUNCTUATION+BENGALI_NUMERALS))

if __name__ == "__main__":
    print(punctuation_remover("১২    জন"))