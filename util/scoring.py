import math
from collections import defaultdict, OrderedDict


def get_cluster_terms(cluster, data):
    terms = {}
    for cluster_index, (documents, _) in cluster.items():
        cluster_terms = []
        term_set = set()
        for document_index in documents:
            document = data[int(document_index[1:]) - 1]
            words = document.split()
            for word in words:
                if word not in term_set:
                    cluster_terms.append(word)
                    term_set.add(word)
        terms[cluster_index] = cluster_terms
    return terms


def calculate_term_probability(data, cluster, terms):
    cluster_scores = {}
    all_terms = []
    for document in data:
        all_terms.extend(document.split())
    all_terms = list(OrderedDict.fromkeys(all_terms))

    for cluster_index, cluster_info in cluster.items():
        cluster_documents, cluster_frequency = cluster_info
        term_frequency = OrderedDict()

        for term in all_terms:
            frequency = sum(
                [1 for document in data if term in document.split()])
            term_frequency[term] = frequency

        total_terms = sum(term_frequency.values())

        all_term_probability = {}
        for term, frequency in term_frequency.items():
            term_probability = (frequency + 0.5) / \
                (total_terms + 0.5 * len(term_frequency))
            # print(f"Cluster {cluster_index}, Term: {term}, Frequency: {frequency}, Probability: {term_probability}")
            all_term_probability[term] = {
                'frequency': frequency,
                'probability': term_probability
            }

    return all_term_probability, total_terms


def scoring_cluster(all_term_probability, data, clusters):
    cluster_words = {}
    cluster_score = {}
    for cluster, documents in clusters.items():
        doc_indices = documents[0]
        words = [word for doc_index in doc_indices for word in data[int(
            doc_index[1:])-1].split()]
        cluster_words[cluster] = words

    for cluster, words in cluster_words.items():
        total_score = 0
        for word in words:
            score = math.exp(-all_term_probability[word]['probability'])
            total_score += score
        cluster_score[cluster] = total_score

    return cluster_score


def scoring(cluster, data):
    terms = get_cluster_terms(cluster, data)
    probability_terms, total_terms = calculate_term_probability(
        data, cluster, terms)
    score = scoring_cluster(probability_terms, data, cluster)
    sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)
    return sorted_score


def main():
    data = [
        "penularan virus elon musk corona meningkat indonesia",
        "pemerintah mengeluarkan kebijakan pembatasan sosial berskala besar",
        "peningkatan kasus positif covid-19 mengkhawatirkan elon musk",
        "vaksinasi massal dilaksanakan pusat-pusat kesehatan",
        "rumah sakit mulai kelebihan kapasitas lonjakan pasien covid-19",
        "protokol kesehatan tetap diikuti memutus rantai penyebaran virus",
        "masyarakat diimbau menggunakan masker beraktivitas luar rumah",
        "pemerintah melakukan upaya mempercepat distribusi vaksin covid-19",
        "pertumbuhan ekonomi terhambat pandemi covid-19",
        "diperlukan kerja sama pihak mengatasi pandemi",
        "kegiatan belajar mengajar dilakukan secara daring mencegah penyebaran virus",
        "peningkatan jumlah tes covid-19 mendeteksi kasus akurat",
        "edukasi pentingnya vaksinasi melindungi diri orang lain elon musk",
        "pemerintah memberlakukan karantina wilayah mengendalikan penyebaran virus",
        "pertemuan massa dihindari mengurangi risiko penularan",
        "pandemi covid-19 berdampak signifikan sektor pariwisata",
        "penyakit menular perlu waspada mengikuti anjuran pemerintah"
    ]

    cluster = {
        'virus': (['D6', 'D1', 'D11', 'D14'], 0.35),
        'pemerintah': (['D2', 'D14', 'D17', 'D8'], 0.69),
        'covid-19': (['D3', 'D5', 'D16', 'D9', 'D12', 'D8'], 0.35)
    }

    # data = [
    # "ahok modus manipulasi ktp",
    # "ahok modus manipulasi ktp",
    # "jokowi rapat natuna",
    # "jokowi rapat natuna",
    # "panglima tni koordinasi natuna ri"
    # ]

    # cluster = {
    # 'klaster1': (['D1', 'D2'], 0.35),
    # 'klaster2': (['D3', 'D4'], 0.35),
    # 'klaster3': (['D5'], 0.35)
    # }

    scoring(cluster, data)


if __name__ == "__main__":
    main()
