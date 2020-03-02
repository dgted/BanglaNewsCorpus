import docx
from bengali_stemmer.rafikamal2014 import RafiStemmer
import string
import pandas as pd
import gensim
import csv

def read_doc_as_pandasDF(filename):

    data = pd.read_csv(filename, error_bad_lines=False)
    data_text = data[['content']]

    data_text['index'] = data_text.index
    documents = data_text

    return(documents)
def punctuation_remover(text):
    BENGALI_PUNCTUATION = string.punctuation + "—।’‘"
    BENGALI_NUMERALS = "০১২৩৪৫৬৭৮৯"
    return text.translate(str.maketrans(' ', ' ', BENGALI_PUNCTUATION+BENGALI_NUMERALS))
def load_stop_word(doc_dir = r"Preprocessing\stopword-dictionary.docx"):

    stop_directory = doc_dir

    doc = docx.Document(stop_directory)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)

    bengali_stop_words = fullText[0].split()
    bengali_stop_words = frozenset(bengali_stop_words)

    return bengali_stop_words
def preprocess_documents(doc):

    preprocessed_list_of_docs = []
    stemmer = RafiStemmer()

    stop_words = load_stop_word()
    preprocessed_docs = []

    doc_token = []

    if isinstance(doc, str):
        for token in punctuation_remover(doc).split():
            if token not in stop_words and len(token) >= 3:
                if len(stemmer.stem_word(token)) >= 2:
                    doc_token.append(stemmer.stem_word(token))


    return doc_token
def prepare_bag_of_words(processed_docs, dictionary):
    return [dictionary.doc2bow(doc) for doc in processed_docs]
def prepare_bow_list(bow_corpus, dictionary):

    header_list = list(range(0, len(dictionary)-1))
    all_list = [header_list]

    for each_list in bow_corpus:
        temp_list = [0]*len(dictionary)
        for each_tuple in each_list:
            temp_list[each_tuple[0]] = each_tuple[1]
        all_list.append(temp_list)

    minimal_all_list = []

    minimal_header_list = []

    for i in range(len(dictionary)):
        minimal_header_list.append(dictionary[i])

    minimal_all_list.append(minimal_header_list)

    for each_mini_list in all_list[1:]:
        minimal_all_list.append(each_mini_list)


    return(minimal_all_list)   
def process_nonstemmed_documents(doc):
    preprocessed_list_of_docs = []

    stop_words = load_stop_word()
    preprocessed_docs = []

    doc_token = []

    if isinstance(doc, str):
        for token in punctuation_remover(doc).split():
            if token not in stop_words and len(token) >= 3:
                doc_token.append((token))


    return doc_token

def get_bow_list(bow_corpus, dictionary):

    full_list  = [['token', 'count']]
    token_list = [0]*len(dictionary)


    for each_doc in bow_corpus:
        for each_tuple in each_doc:
            token_list[each_tuple[0]] += each_tuple[1]

    for i, token_count in enumerate(token_list):
        full_list.append([dictionary[i], token_count])

    return(full_list)

if __name__ == "__main__":
    CSV_LOCATION = r"Datasets\70K-Article\70k_bangla_newspaper.csv"
    
    pd_document = read_doc_as_pandasDF(CSV_LOCATION)

    smaller_documents = pd_document[:20]
    #processed_docs = smaller_documents['content'].map(preprocess_documents)
    processed_docs = smaller_documents['content'].map(process_nonstemmed_documents)


    dictionary = gensim.corpora.Dictionary(processed_docs)
    #dictionary.filter_extremes(no_below=.01, no_above=0.6, keep_n=100000)

    bow_corpus = prepare_bag_of_words(processed_docs, dictionary)

    #print(bow_corpus)

    minimal_all_list = get_bow_list(bow_corpus, dictionary)

    
    with open("test_bow_uni.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(minimal_all_list)
    