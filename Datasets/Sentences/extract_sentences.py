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

def get_sentence_list(pd_document):
    sentence_list = []
    for each_article in smaller_documents['content']:
            #print("Running")
            if(isinstance(each_article, str)):
                for each_line in each_article.split("।"):
                    for each_line_2 in each_line.split("?"):
                        sentence_list.append(each_line_2)


    full_sentence_list = []
    for each_sentence in sentence_list:
        if (not each_sentence == ""):
            full_sentence_list.append(each_sentence)

    return(full_sentence_list)

def write_sentence_to_csv(sentence_list, SENTENCE_LIST_CSV_DIR):

    sentence_df = pd.DataFrame(sentence_list, columns=['content'])
    sentence_df.to_csv(SENTENCE_LIST_CSV_DIR, sep=',',index=False)

    return


if __name__ == "__main__":
    CSV_LOCATION = r"Datasets\70K-Article\70k_bangla_newspaper.csv"
    SENTENCE_CSV_LOCATION = ""
    
    pd_document = read_doc_as_pandasDF(CSV_LOCATION)

    smaller_documents = pd_document[:5]
    #processed_docs = smaller_documents['content'].map(preprocess_documents)

    sentence_list = get_sentence_list(smaller_documents)

    print("="*30)

    print(len(sentence_list))

    
    write_sentence_to_csv(sentence_list, "sentence.csv")

