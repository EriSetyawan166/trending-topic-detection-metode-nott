import mysql.connector
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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

plt.figure(figsize=(15, 15))
wc = WordCloud(width=1000, height=400, max_words=3000).generate(" ".join(df['text']))
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig('assets/img/wordcloud', bbox_inches='tight')
# plt.show()
