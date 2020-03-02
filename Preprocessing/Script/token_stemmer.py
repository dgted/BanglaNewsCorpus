from bengali_stemmer.rafikamal2014 import RafiStemmer
stemmer = RafiStemmer()
stemmed_word = stemmer.stem_word('বাংলায়')
print(stemmed_word)