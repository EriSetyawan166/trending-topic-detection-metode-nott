import mysql.connector
import re
import string
import nltk
from cleantext import clean
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="deteksi_trending_topik"
)

temp = []
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM dokumen WHERE text_bersih = ''")
myresult = mycursor.fetchall()

mycursor1 = mydb.cursor()
mycursor1.execute("SELECT * FROM kamus")
myresult1 = mycursor.fetchall()

factory = StemmerFactory()
stemmer = factory.create_stemmer()

nltk.download('stopwords')

stop_words = set(stopwords.words('indonesian'))
more_stopwords = ['the', 'iya', 'bang', 'sih', 'loh']
stop_words.update(more_stopwords)


for x in myresult:
    # Menghapus tag, hashtag, link URL, spasi, emoticon, dan tanda baca
    bersih = re.sub("@[A-Za-z0-9_]+", "", x[2])
    bersih = re.sub("#[A-Za-z0-9_]+", "", bersih)
    bersih = re.sub(r'http\S+', '', bersih)
    bersih = re.sub("RT : ", "", bersih)
    bersih = " ".join(bersih.split())
    bersih = clean(bersih, no_emoji=True)
    bersih = bersih.translate(str.maketrans('', '', string.punctuation))

    # Mengubah kata informal menjadi formal
    s = ''
    bersih = bersih.split()

    for y in bersih:
        for x1 in myresult1:
            if y == x1[1]:
                y = x1[2]
        s = s + y + " "
        bersih = s

    # Stem the sentence using Sastrawi
    bersih = stemmer.stem(str(bersih))

    # Remove stopwords using NLTK
    filtered_words = [word for word in bersih.split() if word.casefold() not in stop_words]
    bersih = ' '.join(filtered_words)

    query = "SELECT id FROM dokumen WHERE text_bersih=%s"
    mycursor.execute(query, (bersih,))

    s = [i for i in mycursor]

    if s == []:
        mycursor.execute("UPDATE dokumen SET text_bersih=%s WHERE id = %s", (bersih, x[0]))
    else:
        id_s = s[0][0]
        if id_s != x[0]:
            mycursor.execute("DELETE FROM dokumen WHERE id=%s", (x[0],))

mydb.commit()
