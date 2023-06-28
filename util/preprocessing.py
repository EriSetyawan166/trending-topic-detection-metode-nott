import mysql.connector
import re
import string
from cleantext import clean
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

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

stop_factory = StopWordRemoverFactory()
stopword = stop_factory.create_stop_word_remover()

for x in myresult:
    #menghapus tag, hastag, link url, space, emoticon, dan tanda baca
    bersih = re.sub("@[A-Za-z0-9_]+","", x[2])
    bersih = re.sub("#[A-Za-z0-9_]+","", bersih)
    bersih = re.sub(r'http\S+', '', bersih)
    bersih = re.sub("RT : ", "", bersih)
    bersih = " ".join(bersih.split())
    bersih = clean(bersih, no_emoji=True)
    bersih = bersih.translate(str.maketrans('', '', string.punctuation))

    #mengubah kata informal menjadi formal
    s = ''
    bersih = bersih.split()
    # print(bersih)
    
    for y in bersih:
        for x1 in myresult1:
            if y == x1[1] :
                y = x1[2]
        s = s + y + " "
        bersih = s 

    bersih = stemmer.stem(str(bersih))
    bersih = stopword.remove(bersih)

    query = "SELECT id FROM dokumen WHERE text_bersih=%s"
    mycursor.execute(query, (bersih,))

    s = [i for i in mycursor]

    if s == []:
    # mycursor.execute("INSERT INTO tweet_bersih (id, user_screen_name, text, sentiment) VALUES (%s ,%s, %s, %s)", (x[0], x[1], bersih, x[3]))
        mycursor.execute("UPDATE dokumen set text_bersih=%s WHERE id = %s", (bersih, x[0]))
    # UPDATE tweet2 SET sentiment=$hasil WHERE id=$id
    
    else:
        id_s = s[0][0]
        if(id_s != x[0]):
            mycursor.execute("DELETE FROM dokumen WHERE id=%s", (x[0],))
   
mydb.commit()
