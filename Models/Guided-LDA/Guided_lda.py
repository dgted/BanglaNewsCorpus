import docx
from bengali_stemmer.rafikamal2014 import RafiStemmer
import string
import pandas as pd
import gensim
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
def boost_words_in_eta(eta, dictionary, boost_words):
    for i, word_list in enumerate(boost_words):
        boost_word_id_list = []
        print("{} is in {}".format(i, word_list))


        uniq, count = np.unique(eta, return_counts=True)
        print(dict(zip(uniq, count)))

        #print([list(dictionary.keys())[list(dictionary.values()).index(each_word)] for each_word in word_list])

        for each_word in word_list:

            try:
                word_id = list(dictionary.keys())[list(dictionary.values()).index(each_word)]
                print(word_id)
                boost_word_id_list.append(word_id)

            except ValueError:
                print("{} Not found in Dictionary ".format(each_word))

        for word in boost_word_id_list:
            eta[i][word] = 0.75

    uniq, count = np.unique(eta, return_counts=True)
    print(dict(zip(uniq, count)))

    return eta
def prepare_model_list_presentation(lda_model, dictionary):

    header_list =  [lda_model.id2word[i] for i in range(0, len(dictionary))]
    list_for_csv = [header_list]

    for i in range(lda_model.num_topics):
        each_topic_list = lda_model.get_topic_terms(i, topn=len(dictionary))
        sorted_each_topic_list = sorted(each_topic_list, key=lambda k: k[0])
        just_value_list = [each_tuple[1] for each_tuple in sorted_each_topic_list]

        list_for_csv.append(just_value_list)

    return(list_for_csv)
def prepare_guided_lda_model(bow_corpus, num_topics, dictionary):
    lda_model_guided = prepare_guided_lda_model(bow_corpus, num_topics=NUM_TOPICS, dictionary=dictionary)
    return lda_model_guided

if __name__ == "__main__":
    np.random.seed(2019)

    NUM_TOPICS = 6
    CSV_LOCATION = r"Datasets\70K-Article\70k_bangla_newspaper.csv"
    
    pd_document = read_doc_as_pandasDF(CSV_LOCATION)

    smaller_documents = pd_document[:5]
    processed_docs = smaller_documents['content'].map(preprocess_documents)

    dictionary = gensim.corpora.Dictionary(processed_docs)
    #dictionary.filter_extremes(no_below=.01, no_above=0.6, keep_n=100000)

    bow_corpus = prepare_bag_of_words(processed_docs, dictionary)

    #print(bow_corpus)
    eta = np.ones((NUM_TOPICS, len(dictionary))) * 0.01
    # print("Shape of eta is {}".format(eta.shape))
    # print("type of dictionary {}".format(type(dictionary)))
    # print(eta)
    boost_words =[
        ['অধিনায়ক', 'মেসি', 'ক্রিকেট', 'জাতীয়', 'রান', 'উইকেট'],
        ['মূলধন', 'বিনিয়োগ', 'শেয়ার', 'আইন', 'টাকা', 'শতাংশ', 'ব্যাংক', 'পণ্য']

    ]
    boosed_eta = boost_words_in_eta(eta, dictionary, boost_words)
    lda_model_guided = gensim.models.LdaMulticore(bow_corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=2, workers=3, eta=eta)
    print("Guided LDA Model:")

    for idx in range(NUM_TOPICS):
            # Print the first 10 most representative topics
        print("Topic #%s:" % idx, lda_model_guided.print_topic(idx, 10))

    print("=" * 20)

    model_to_csv = prepare_model_list_presentation(lda_model_guided, dictionary)

    with open("guided_lda_Model_to_csv2.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(model_to_csv)


