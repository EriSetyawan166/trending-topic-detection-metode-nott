from util import connect_db
from util import ftc
from util import scoring
from util.lda import LDA
import nltk
import random

def pre_process_documents(doc):
    wpt = nltk.WordPunctTokenizer()
    for i in range(len(doc)):
        # Tokenisasi dokumen
        tokens = wpt.tokenize(doc[i][0])
        # Filter stopwords dari dokumen
        # Menyimpan dokumen yang telah diproses
        doc[i] = tokens
    return doc

def fetch_data():
    # Connect to the database
    conn, cursor = connect_db("localhost", "root", "",
                              "deteksi_trending_topik")

    # Execute a query to fetch preprocessed text from the dokumen table
    cursor.execute("SELECT preproccess_text FROM dokumen_backup LIMIT 200")
    rows = cursor.fetchall()

    # Extract the preprocessed text from the rows and store in a list
    preprocessed_text_list = [row[0] for row in rows]

    # Close the database connection
    cursor.close()
    conn.close()

    # Return the preprocessed text as an array
    return preprocessed_text_list


def main():
    # Fetch the preprocessed text from the database
    data = fetch_data()

    # data = [
    # "penularan virus elon musk corona meningkat indonesia",
    # "pemerintah mengeluarkan kebijakan pembatasan sosial berskala besar",
    # "peningkatan kasus positif covid mengkhawatirkan elon musk",
    # "vaksinasi massal dilaksanakan pusat-pusat kesehatan",
    # "rumah sakit mulai kelebihan kapasitas lonjakan pasien covid",
    # "protokol kesehatan tetap diikuti memutus rantai penyebaran virus",
    # "masyarakat diimbau menggunakan masker beraktivitas luar rumah",
    # "pemerintah melakukan upaya mempercepat distribusi vaksin covid",
    # "pertumbuhan ekonomi terhambat pandemi covid",
    # "diperlukan kerja sama pihak mengatasi pandemi",
    # "kegiatan belajar mengajar dilakukan secara daring mencegah penyebaran virus",
    # "peningkatan jumlah tes covid mendeteksi kasus akurat",
    # "edukasi pentingnya vaksinasi melindungi diri orang lain elon musk",
    # "pemerintah memberlakukan karantina wilayah mengendalikan penyebaran virus",
    # "pertemuan massa dihindari mengurangi risiko penularan",
    # "pandemi covid berdampak signifikan sektor pariwisata",
    # "penyakit menular perlu waspada mengikuti anjuran pemerintah"
    # ]   

    # # Print the preprocessed text to the console
    # print(data)

    cluster = ftc(data, 4)
    # print(cluster)
    print("Cluster:")
    for term_set, document in cluster.items():
        print(document[0], end=', ')

    print("\n\nDeksripsi cluster")
    for term_set, document in cluster.items():
        print(f"{{{''.join(term_set)}}}", end=", ")

    scoring_cluster = scoring(cluster, data)
    print("\n\nHasil Skoring")
    print(scoring_cluster)
    
    # Get the cluster key with the highest score
    highest_score_key = max(scoring_cluster, key=lambda x: x[1])

    # Get the documents from the cluster with the highest score
    documents = cluster[highest_score_key[0]][0]
    selected_documents = [[data[int(doc[1:])-1]] for doc in documents]
    # print(selected_documents)
    # Memproses dokumen menggunakan fungsi pre_process_documents
    pre_processed_documents = pre_process_documents(selected_documents)

    # Membuat objek LDA
    lda = LDA(K=2, max_iteration=1000)

    # Menjalankan LDA pada dokumen yang telah diproses
    result = lda.run(pre_processed_documents)

    # Mendapatkan daftar kata kunci untuk setiap topik
    topic_word_list = lda.get_topic_word_list()
    print("\nPenentuan topik:")
    print(topic_word_list)

    sentence = set(word for words in topic_word_list.values() for word in words)


    print("\nTrending topik:")
    print(sentence)
        
if __name__ == "__main__":
    main()
