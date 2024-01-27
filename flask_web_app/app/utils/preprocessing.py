# file ini berisi fungsi untuk membersihkan data text
import re
import nltk
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def data_preprocessing(text):
    lm = WordNetLemmatizer() # init lemma
    stop_words = set(stopwords.words('english')) # init stopword
    text = text.lower() # mengubah text ke lowercase
    text = re.sub(r'^a-zA-Z0-9', ' ', text) # karakter selain huruf dan angka akan dihapus
    text = re.sub(r'<.*?>', ' ', text) # tag html akan dihapus
    text = "".join([x for x in text if x not in string.punctuation]) # filter kata dari punctuation (tanda baca)
    text = text.split()
    text = [lm.lemmatize(x) for x in text if x not in stop_words] # filter kata dari stopwords (kata yang tidak penting) kemudian kata tersebut diubah ke bentuk dasarnya menggunakan lemmatizer
    text = " ".join(text)
    return text
