from util import connect_db
from util import ftc
from util import scoring


def fetch_data():
    # Connect to the database
    conn, cursor = connect_db("localhost", "root", "",
                              "deteksi_trending_topik")

    # Execute a query to fetch preprocessed text from the dokumen table
    cursor.execute("SELECT preproccess_text FROM dokumen LIMIT 200")
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
    # "peningkatan kasus positif covid-19 mengkhawatirkan elon musk",
    # "vaksinasi massal dilaksanakan pusat-pusat kesehatan",
    # "rumah sakit mulai kelebihan kapasitas lonjakan pasien covid-19",
    # "protokol kesehatan tetap diikuti memutus rantai penyebaran virus",
    # "masyarakat diimbau menggunakan masker beraktivitas luar rumah",
    # "pemerintah melakukan upaya mempercepat distribusi vaksin covid-19",
    # "pertumbuhan ekonomi terhambat pandemi covid-19",
    # "diperlukan kerja sama pihak mengatasi pandemi",
    # "kegiatan belajar mengajar dilakukan secara daring mencegah penyebaran virus",
    # "peningkatan jumlah tes covid-19 mendeteksi kasus akurat",
    # "edukasi pentingnya vaksinasi melindungi diri orang lain elon musk",
    # "pemerintah memberlakukan karantina wilayah mengendalikan penyebaran virus",
    # "pertemuan massa dihindari mengurangi risiko penularan",
    # "pandemi covid-19 berdampak signifikan sektor pariwisata",
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


if __name__ == "__main__":
    main()
