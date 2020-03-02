import docx
from bengali_stemmer.rafikamal2014 import RafiStemmer
import string
import pandas as pd
import gensim
from gensim.models.coherencemodel import CoherenceModel
from gensim.models import Word2Vec
from nltk.cluster import KMeansClusterer
import nltk
import csv
import numpy as np

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
def write_cluster_to_txt(model, assigned_clusters, num_cluster):

    words = list(model.wv.vocab)


    for i, word in enumerate(words):
        file_name = "cluster_"+str(assigned_clusters[i])+".txt"
        temp_file = open(file_name, "a",  encoding="utf-8")
        temp_file.write(word + "\n")
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

if __name__ == "__main__":
    np.random.seed(2019)
    NUM_CLUSTERS=6

    CSV_LOCATION = r"Datasets\70K-Article\70k_bangla_newspaper.csv"
    
    pd_document = read_doc_as_pandasDF(CSV_LOCATION)

    smaller_documents = pd_document[:5]
    processed_docs = smaller_documents['content'].map(preprocess_documents)
    #processed_docs = smaller_documents['content'].map(process_nonstemmed_documents)


    #dictionary = gensim.corpora.Dictionary(processed_docs)
    #dictionary.filter_extremes(no_below=.01, no_above=0.6, keep_n=100000)

    #bow_corpus = prepare_bag_of_words(processed_docs, dictionary)

    sentences = processed_docs.to_list()

    #Print Cluster
    model = Word2Vec(sentences, min_count=1)
    X = model[model.wv.vocab]


    kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
    assigned_clusters = kclusterer.cluster(X, assign_clusters=True)
    print ("done")

    write_cluster_to_txt(model, assigned_clusters, 6)



