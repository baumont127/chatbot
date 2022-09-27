import pandas as pd
import sqlite3
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import spacy
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from django.core.cache import cache


nlp = spacy.load('fr_core_news_md')


def clean_text(text):
    with open("/home/merouane/Gitlab/Ecole_IA/projet-5-groupe-3/Veille_IA/utils/stop_words_french.txt") as file:
        stop_words = file.read()
    stop_words = stop_words.split()
    
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.match('[a-zA-Z]', token):
            filtered_tokens.append(token)
            
    token_text=" ".join(filtered_tokens)
    #Lemmatizations
    doc = nlp(token_text)
    cleaned_text = [token.lemma_ for token in doc if str(token) not in stop_words and len(str(token))>3]
    cleaned_text = " ".join(cleaned_text)
    cleaned_text = cleaned_text.lower()
    return cleaned_text

def get_clean_data(id_user)-> pd.DataFrame: 
    querry = "SELECT rs.id, rs.user_id, corpus, lien FROM app_veille_ressource AS rs INNER JOIN app_veille_type_ressource AS tr ON rs.ressource_id = tr.id WHERE tr.name ='Article' AND rs.user_id = {id_user};".format(id_user=id_user)
    con = sqlite3.connect("/home/merouane/Gitlab/Ecole_IA/projet-5-groupe-3/Veille_IA/db.sqlite3")
    df = pd.read_sql_query(sql=querry, con=con)
    df["cleaned_data"] = df["corpus"].map(clean_text)

    return df

def get_vocabulary(df)-> list:
    
    vocabulary = set()
 
    for doc in df.cleaned_data:
        vocabulary.update(doc.split(' '))
    vocabulary = list(vocabulary)

    return vocabulary

def tfidf_vectorizer(df, vocabulary):
    with open("/home/merouane/Gitlab/Ecole_IA/projet-5-groupe-3/Veille_IA/utils/stop_words_french.txt") as file:
        stop_words = file.read()
    stop_words = stop_words.split()

    vectorizer = TfidfVectorizer(stop_words=stop_words, vocabulary=vocabulary)
    X = vectorizer.fit_transform(df["cleaned_data"])

    return vectorizer, X

def gen_vector_T(tokens, vectorizer, vocabulary):
    Q = np.zeros((len(vocabulary)))   
    x= vectorizer.transform(tokens)
    #print(tokens[0].split(','))
    for token in tokens:
        try:
            ind = vocabulary.index(token)
            Q[ind] = x[0, vectorizer.vocabulary_[token]]
        except:
            pass
    return Q

def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

def cosine_similarity_T(X, k, query, vectorizer, vocabulary, df):
    preprocessed_query = preprocessed_query = re.sub("\W+", " ", query).strip()
    tokens = word_tokenize(str(preprocessed_query))
    q_df = pd.DataFrame(columns=['q_clean'])
    q_df.loc[0,'q_clean'] =tokens
    q_df['q_clean'] = clean_text(tokens[0])
    d_cosines = []
    query_vector = gen_vector_T(q_df['q_clean'], vectorizer, vocabulary)
    for d in X.A:

        d_cosines.append(cosine_sim(query_vector, d))

                    
    out = np.array(d_cosines).argsort()[-k:][::-1]
    #print("")
    d_cosines.sort()
    a = pd.DataFrame()
    for i,index in enumerate(out):
        a.loc[i,'id'] = df['id'][index]
        a.loc[i,'Subject'] = df['lien'][index]
    for j,simScore in enumerate(d_cosines[-k:][::-1]):
        a.loc[j,'Score'] = simScore
    return a

def pipeline_tfidf(user_id):
    print(user_id)
    print("collect data...")
    df = get_clean_data(user_id)
    print("get vocabulary...")
    vocabulary = get_vocabulary(df)
    print("test", vocabulary)
    print("TF-IDF vectorization...")
    vectorizer, X = tfidf_vectorizer(df, vocabulary)
    cache.set('vectorizer', vectorizer)
    cache.set('vocabulary', vocabulary)
    cache.set('X', X)
    cache.set('df', df)
    print("Done")

