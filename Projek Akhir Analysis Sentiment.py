# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MImF6QI24Lxi1PsWtvT2I6lbb7XbTtAu
"""

!pip install google-play-scraper

"""<h2> Import Libary"""

from google_play_scraper import app

import pandas as pd

import numpy as np

"""<h2> Scraping Data"""

# scrap available review

from google_play_scraper import Sort, reviews

result, continuation_token  = reviews (
'com.gojek.app',
lang= 'id',
country= 'id',
sort= Sort.NEWEST,
count= 20000,
filter_score_with= None
)

df_gojek = pd.DataFrame(np.array(result),columns=['review'])

df_gojek = df_gojek.join(pd.DataFrame(df_gojek.pop('review').tolist()))

df_gojek.head()

df_gojek.tail()

len(df_gojek.index)

data_new = df_gojek[['userName', 'score', 'at', 'content']]
data_new.head()

data_new = df_gojek[['userName', 'score', 'at', 'content']]
data_new.tail()

#save data to folder
data_new.to_csv("datagojek.csv", index=False)

path = '\\Documents\\Analisis Sentimen Gojek\\Data File\\'

"""<h1> Preprocessing

**Loading Data Frame**
"""

df = pd.read_csv("datagojek.csv")


df

df.info()

df = df.drop(df.loc[df['score'] == 3].index)
df

"""<h1> Labelling Data"""

def pelabelan(rate):
    if rate <= 2 :
        return 'negatif'
    else:
        return 'positif'

df['label'] = df['score'].apply(pelabelan)
df

"""<h1>Preprocessing"""

import nltk

# mengubah data pada column content menjadi string agar dapat melakukan pemrosesan data teks
df['content'] = df['content'].astype(str)

df.info()

"""<h1> Cleansing"""

import re
import string

def remove_links(text):
    # menghapus tab, new line, ans back slice
    text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
    # menghapus non ASCII (emoticon, chinese word, .etc)
    text = text.encode('ascii', 'replace').decode('ascii')
    # menghapus mention, link, hashtag
    text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
    # menghapus URL
    return text.replace("http://", " ").replace("https://", " ")

df['content'] = df['content'].apply(remove_links)

#menghapus number
def remove_number(text):
    return  re.sub(r"\d+", " ", text)

df['content'] = df['content'].apply(remove_number)

#menghapus punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans("","",string.punctuation))

df['content'] = df['content'].apply(remove_punctuation)

# menghapus single char
def remove_singl_char(text):
    return re.sub(r"\b[a-zA-Z]\b", " ", text)

df['content'] = df['content'].apply(remove_singl_char)

# menghapus number how to fix it
def remove_number(text):
    return re.sub(r"\d+", " ", text)

df['content'] = df['content'].apply(remove_number)

df

"""<h1> Case Folding"""

df['content'] = df['content'].str.lower()

df

"""<h1> Tokenize"""

import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

nltk.download('punkt')

def word_tokenize_wrapper(text):
    return word_tokenize(text)

df['content_tokenize'] = df['content'].apply(word_tokenize_wrapper)

df

# Menghitung Distibusi Persebaran Kata
def freqDist_wrapper(text):
    return FreqDist(text)

content_fqsist = df['content_tokenize'].apply(freqDist_wrapper)

print('Frequency Tokens : \n')
print(content_fqsist.head().apply(lambda x : x.most_common()))

"""<h1> Normalisasi"""

slank_word_dict = {

    }

def slank_normalized_term(document):
    return [slank_word_dict[term] if term in slank_word_dict else term for term in document]

normalizad_word = pd.read_table("https://raw.githubusercontent.com/evrintobing17/NormalisasiKata/master/kbba.txt")

normalizad_word_dict = {}

for index, row in normalizad_word.iterrows():
    if row[0] not in normalizad_word_dict:
        normalizad_word_dict[row[0]] = row[1]

def normalized_term(document):
    return [normalizad_word_dict[term] if term in normalizad_word_dict else term for term in document]

normalizad_word = pd.read_csv("https://raw.githubusercontent.com/IndianiTiosari01/Proyek-KuliahPM-NormalisasiKata/master/kamus_alay.csv")

normalizad_word_dict = {}

for index, row in normalizad_word.iterrows():
    if row[0] not in normalizad_word_dict:
        normalizad_word_dict[row[0]] = row[1]

def normalized_term(document):
    return [normalizad_word_dict[term] if term in normalizad_word_dict else term for term in document]

df['content_normalized'] = df['content_tokenize'].apply(normalized_term).apply(slank_normalized_term)

df

"""<h1> Stopword Removal"""

from nltk.corpus import stopwords

import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

nltk.download('punkt')

nltk.download('stopwords')

list_stopwords = stopwords.words('indonesian')

def word_tokenize_wrapper(text):
    return word_tokenize(text)

df['content_tokenize'] = df['content'].apply(word_tokenize_wrapper)

#remove stopword pada list token
def stopwords_removal(words):
    return [word for word in words if word not in list_stopwords]

df['content_stop_removed'] = df['content_normalized'].apply(stopwords_removal)

df

"""<h1> Stemming"""

pip install sastrawi

pip install swifter

# import Sastrawi package
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import swifter


# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# stemmed
def stemmed_wrapper(term):
    return stemmer.stem(term)

term_dict = {}

for document in df['content_stop_removed']:
    for term in document:
        if term not in term_dict:
            term_dict[term] = ' '

for term in term_dict:
    term_dict[term] = stemmed_wrapper(term)
    print(term,":" ,term_dict[term])

# apply stemmed term to dataframe
def get_stemmed_term(document):
    return [term_dict[term] for term in document]

df['content_Stemmed'] = df['content_stop_removed'].swifter.apply(get_stemmed_term)

df.to_csv("data_cleangojek.csv", index = False)

"""<h1> Data clean

**Import Library**
"""

import pandas as pd
import numpy as np

#plot Grafik
import matplotlib.pyplot as plt
import missingno as msno

df = pd.read_csv("data_cleangojek.csv")
display(df)

df["label"].value_counts()

def sentimen(data:int):
  if data > 0:
    return "positif"
  elif data < 0:
    return "negatif"
  else:
    return "netral"

df_ = pd.read_csv('data_cleangojek.csv')

# Plot the histogram
sns.histplot(data=df_, x="label")

"""<h1> Oversampling"""

from sklearn.utils import resample
df_majority = df[(df['label']=="positif")]
df_minority = df[(df['label']=="negatif")]

df_minority_upsampled = resample(df_minority,
                                 replace=True,    # sample with replacement
                                 n_samples=12914, # to match majority class
                                 random_state=42)  # reproducible results

df_upsampled = pd.concat([df_minority_upsampled, df_majority])

df_upsampled["label"].value_counts()

"""<h1> Transformation"""

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
tfidf_stemmed = vectorizer.fit_transform(df['content_Stemmed'])
dense= tfidf_stemmed.toarray()

"""<h1> Text Mining

**Data Splitting**
"""

from sklearn.model_selection import train_test_split

X_train1, X_test1, Y_train1, Y_test1 = train_test_split(dense, df['label'], test_size = 0.1, random_state= 42)

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
y_pred = gnb.fit(X_train1,Y_train1)

"""<h1> Evaluasi"""

from sklearn.metrics import confusion_matrix

evaluasi = gnb.predict(X_test1)
print(confusion_matrix(Y_test1, evaluasi))

from sklearn.metrics import accuracy_score
print(accuracy_score(Y_test1, evaluasi))

from sklearn.metrics import classification_report
print(classification_report(Y_test1, evaluasi))

import matplotlib.pyplot as plt
from jcopml.plot import plot_confusion_matrix


plot_confusion_matrix(X_train1, Y_train1, X_test1, Y_test1, gnb)
plt.show()

from sklearn import metrics

confusion_matrix = metrics.confusion_matrix(Y_test1, evaluasi)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix)

cm_display.plot()
plt.show()