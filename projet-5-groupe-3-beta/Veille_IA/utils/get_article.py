from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import spacy
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from boilerpy3 import extractors
import requests
import justext
from goose3 import Goose


nlp = spacy.load('fr_core_news_md')

def get_title(link: str):
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    req = Request(link, headers=hdr)
    html = urlopen(req).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1').text

    return title

def get_corpus_article(link: str):
    """
    Get the article from the link and return the text"""

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
    req = Request(link, headers=hdr)
    html = urlopen(req).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    
    links = [e.get_text() for e in soup.find_all('p')]
    article = '\n'.join(links)
    return article

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
    #split into list
    cleaned_text = cleaned_text.split()
    return cleaned_text

def tf_idf(text):
    """
    Get the tf-idf of the text"""
    with open("/home/merouane/Gitlab/Ecole_IA/projet-5-groupe-3/Veille_IA/utils/stop_words_french.txt") as file:
        stop_words = file.read()
    stop_words = stop_words.split()

    vectorizer = TfidfVectorizer(stop_words=stop_words)
    X = vectorizer.fit_transform(text)
    idf = list(vectorizer.vocabulary_.keys())[:10]  
    return idf

def get_article_text(link: str):
    """
    Get the text of the article from the link"""

    extractor = extractors.ArticleExtractor()
    # From a URL
    content = extractor.get_content_from_url(link)

    return content

def get_article_text_just_text(link):

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    response = requests.get(link, headers=hdr)
    paragraphs = justext.justext(response.content, justext.get_stoplist("French"))
    content_text = []
    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            content_text.append(paragraph.text)
    text = ''.join(content_text)
    return text

def get_article_text_goos(link):
    g = Goose({'browser_user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'})
    article = g.extract(url=link)
    return article.cleaned_text
