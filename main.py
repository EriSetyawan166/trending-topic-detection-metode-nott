from util import connect_db
from util import ftc
from util import scoring
from util.lda import LDA
import nltk
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import math
import os
import numpy as np

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

    # Delete existing images
    # image_dir = 'C:/xampp/htdocs/trending topic detection metode nott/assets/img/'
    # for file_name in os.listdir(image_dir):
    #     if file_name.startswith('cluster_') and file_name.endswith('_documents.png'):
    #         os.remove(os.path.join(image_dir, file_name))

    # file_path = 'C:/xampp/htdocs/trending topic detection metode nott/assets/img/cluster_ranking_scores.png'
    # if os.path.exists(file_path):
    #     os.remove(file_path)
   
    print("Cluster:")
    for term_set, document in cluster.items():
        print(document[0], end=', ')

    print("\n\nDeksripsi cluster")
    for term_set, document in cluster.items():
        print(f"{{{''.join(term_set)}}}", end=", ")

    # # Generate document text images for each cluster
    # for i, (term_set, document) in enumerate(cluster.items()):
    #     doc_indices = document[0]  # Get the document indices
    #     cluster_texts = [data[int(idx[1:]) - 1] for idx in doc_indices]  # Get the corresponding document texts
        
    #     # Calculate the required height for the image
    #     line_height = 0.1
    #     image_height = max(len(cluster_texts) * line_height, 5)
        
    #     # Create a new figure with dynamic size
    #     plt.figure(figsize=(10, image_height))
        
    #     # Plot the document texts
    #     for j, text in enumerate(cluster_texts):
    #         plt.text(0.05, 0.9 - j * line_height, text, fontsize=14, ha='left', va='center')
        
    #     # Remove x and y axes
    #     plt.axis('off')
        
    #     # Set plot title
    #     plt.title(f'Cluster {i+1} - {" ".join(term_set)}', fontsize=16)
        
    #     # Save the image
    #     plt.savefig(f'C:/xampp/htdocs/trending topic detection metode nott/assets/img/cluster_{i+1}_documents.png', bbox_inches='tight')
        
    scoring_cluster = scoring(cluster, data)
    # print("\n\nHasil Skoring")
    # print(scoring_cluster)

    # # Mengurutkan scoring_cluster berdasarkan nilai tertinggi
    # scoring_cluster.sort(key=lambda x: x[1], reverse=True)

    # # Extract the keywords and scores from the scoring cluster
    # keywords = [keyword for keyword, _ in scoring_cluster]
    # scores = [score for _, score in scoring_cluster]

    # # Membalik urutan elemen dalam daftar keywords dan scores
    # keywords = keywords[::-1]
    # scores = scores[::-1]

    # # Generate random colors for the bars
    # colors = [tuple(np.random.rand(3)) for _ in keywords]

    # # Plot the scores using a horizontal bar chart with larger figure size
    # plt.figure(figsize=(10, 0.5 * len(keywords))) # Adjust the figure size accordingly
    # plt.barh(keywords, scores, height=0.5, color=colors) # Set the height parameter to adjust the spacing between bars and apply random colors
    # plt.xlabel('Scores')
    # plt.ylabel('Keywords')
    # plt.title('Cluster Ranking Scores')
    # plt.tight_layout()

    # # Add text labels on the right side of each bar
    # for i in range(len(keywords)):
    #     plt.text(scores[i] + 0.5, i, f'{scores[i]:.2f}', va='center')

    # # Save the bar chart image
    # plt.savefig('C:/xampp/htdocs/trending topic detection metode nott/assets/img/cluster_ranking_scores.png', bbox_inches='tight')


    # # Mengurutkan scoring_cluster berdasarkan nilai tertinggi
    # scoring_cluster.sort(key=lambda x: x[1], reverse=True)

    # # Mengambil hanya top 5 nilai teratas
    # top_scores = scoring_cluster[:5]
    # keywords = [keyword for keyword, _ in top_scores]
    # scores = [score for _, score in top_scores]

    # # Generate random colors for the bars
    # colors = [tuple(np.random.rand(3)) for _ in keywords]

    # # Plot the scores using a vertical bar chart with larger figure size
    # plt.figure(figsize=(10, 6)) # Adjust the figure size accordingly
    # plt.bar(keywords, scores, color=colors)
    # plt.xlabel('Keywords')
    # plt.ylabel('Scores')
    # plt.title('Top 5 Cluster Ranking Scores')
    # plt.xticks(rotation=45)
    # plt.tight_layout()

    # # Add text labels on top of each bar
    # for i in range(len(keywords)):
    #     plt.text(i, scores[i] + 0.5, f'{scores[i]:.2f}', ha='center')

    # # Save the bar chart image
    # plt.savefig('C:/xampp/htdocs/trending topic detection metode nott/assets/img/cluster_ranking_scores_top.png', bbox_inches='tight')


    #Get the cluster key with the highest score
    highest_score_key = max(scoring_cluster, key=lambda x: x[1])
    print(highest_score_key)

    # Get the documents from the cluster with the highest score
    documents = cluster[highest_score_key[0]][0]
    selected_documents = [[data[int(doc[1:])-1]] for doc in documents]
    # print(selected_documents)
    # Memproses dokumen menggunakan fungsi pre_process_documents
    pre_processed_documents = pre_process_documents(selected_documents)

    # Membuat objek LDA
    lda = LDA(K=1, max_iteration=1000)

    # Menjalankan LDA pada dokumen yang telah diproses
    result = lda.run(pre_processed_documents)

    # Mendapatkan daftar kata kunci untuk setiap topik
    topic_word_list = lda.get_topic_word_list()
    print("\nPenentuan topik:")
    print(topic_word_list)

    # Ambil nilai (list kata-kata) dari topic_word_list
    topic_words = list(topic_word_list.values())[0]

    # Gabungkan semua kata-kata menjadi satu string
    text = ' '.join(topic_words)

    # Buat objek WordCloud dengan konfigurasi yang diinginkan
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Tampilkan dan simpan WordCloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Detected Topics WordCloud')
    plt.tight_layout()

    # Simpan gambar WordCloud ke file
    output_file = 'assets\img\wordcloud_topic.png'  # Ganti dengan path dan nama file yang diinginkan
    plt.savefig(output_file, bbox_inches='tight')
    
        
if __name__ == "__main__":
    main()


