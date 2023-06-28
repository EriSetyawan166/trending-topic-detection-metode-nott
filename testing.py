import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

nltk.download('stopwords')

stop_words = set(stopwords.words('indonesian'))
more_stopwords = ['pak']
stop_words.update(more_stopwords)

stemmer = SnowballStemmer('indonesian')

sentence = 'Perekonomian anda pak yang Indonesia sedang dalam pertumbuhan yang membanggakan'

tokens = word_tokenize(sentence)

filtered_tokens = [word for word in tokens if word.casefold() not in stop_words]

stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

filtered_sentence = ' '.join(stemmed_tokens)

print(filtered_sentence)
