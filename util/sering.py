from collections import Counter
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="deteksi_trending_topik"
)

text = []

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM dokumen")
myresult = mycursor.fetchall()

for tweet in myresult:
    text.append(tweet[2])

df = pd.DataFrame({'text': text})

count = Counter(" ".join(df['text']).split()).most_common(20)
df_count = pd.DataFrame(count, columns=["teks", "jumlah"])

output = df_count.head()
hasil = output.plot.bar(x='teks', y='jumlah', rot=0)
hasil.get_figure().savefig('assets/img/sering.png')
