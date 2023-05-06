from collections import defaultdict
import operator
from itertools import combinations
from math import log

def generate_all_terms_flat(data):
    word_frequencies = defaultdict(int)
    
    # Preprocessing data and counting word frequencies
    for document in data:
        
        # Count word frequencies
        for word in document.split():
            word_frequencies[word] += 1
    
    # Sort words by frequency in descending order
    sorted_words = sorted(word_frequencies.items(), key=operator.itemgetter(1), reverse=True)
    
    # Select all terms
    all_terms = [word for word, _ in sorted_words]
    
    return all_terms

def find_common_words(all_terms, data, min_support):
    word_counts = defaultdict(int)
    
    # Count word occurrences in the documents
    for document in data:

        # Update word counts
        unique_words = set(document.split())
        for word in unique_words:
            if word in all_terms:
                word_counts[word] += 1
    
    # Find common words based on min_support
    common_words = [word for word, count in word_counts.items() if count >= min_support]
    
    return common_words

def generate_frequent_term_set(common_words, data, min_support):
    frequent_term_set = {}
    
    # Generate combinations of words
    for r in range(1, len(common_words) + 1):
        word_combinations = combinations(common_words, r)
        
        # Check minimum support for each combination
        for combination in word_combinations:
            support_documents = []
            for i, document in enumerate(data):
                
                
                # Check if all words in the combination are present in the document
                if all(word in document for word in combination):
                    support_documents.append(f"D{i + 1}")
            
            # If combination meets the minimum support, add it to frequent term set
            if len(support_documents) >= min_support:
                frequent_term_set[", ".join(combination)] = support_documents
    
    return frequent_term_set

def calculate_entropy_overlap(frequent_term_set, data):
    entropy_overlap_results = {}

    for term_set, documents in frequent_term_set.items():
        entropy_overlap_sum = 0
        for document in documents:
            frequency = sum(document in documents for documents in frequent_term_set.values())
            entropy_overlap = (-1/frequency) * log(1/frequency)
            entropy_overlap_sum += entropy_overlap
        
        entropy_overlap_results[term_set] = (documents, round(entropy_overlap_sum, 2))
        
    return entropy_overlap_results

def remove_document(entropy_overlap_results):
    removed_dict = {}
    lowest_value = float('inf')  # Set initial lowest value to infinity
    lowest_entry = None  # Set initial lowest entry to None

    for term_set, document in entropy_overlap_results.items():
        frequency = document[1]  # Get the frequency
        if frequency < lowest_value:
            lowest_value = frequency
            lowest_entry = {term_set: document}
    
    print(lowest_entry)
    

def main():
    min_support = 2
    # Usage example
    # data = [
    #     "lonjakan kasus corona indonesia",
    #     "vaksinasi indonesia astrazeneca",
    #     "swab antigen vaksin sinovac",
    #     "vaksin corona serentak nasional",
    #     "isolasi mandiri masyarakat terpapar covid"
    # ]
    data = [
    "penularan virus corona meningkat indonesia",
    "pemerintah mengeluarkan kebijakan pembatasan sosial berskala besar",
    "peningkatan kasus positif covid-19 mengkhawatirkan",
    "vaksinasi massal dilaksanakan pusat-pusat kesehatan",
    "rumah sakit mulai kelebihan kapasitas lonjakan pasien covid-19",
    "protokol kesehatan tetap diikuti memutus rantai penyebaran virus",
    "masyarakat diimbau menggunakan masker beraktivitas luar rumah",
    "pemerintah melakukan upaya mempercepat distribusi vaksin covid-19",
    "pertumbuhan ekonomi terhambat pandemi covid-19",
    "diperlukan kerja sama pihak mengatasi pandemi",
    "kegiatan belajar mengajar dilakukan secara daring mencegah penyebaran virus",
    "peningkatan jumlah tes covid-19 mendeteksi kasus akurat",
    "edukasi pentingnya vaksinasi melindungi diri orang lain",
    "pemerintah memberlakukan karantina wilayah mengendalikan penyebaran virus",
    "pertemuan massa dihindari mengurangi risiko penularan",
    "pandemi covid-19 berdampak signifikan sektor pariwisata",
    "penyakit menular perlu waspada mengikuti anjuran pemerintah"
    ]

    all_terms = generate_all_terms_flat(data)
    
    k_terms = find_common_words(all_terms, data, min_support)
    # print(k_terms)
    
    frequent_term_set = generate_frequent_term_set(k_terms, data, min_support)
    # print(frequent_term_set)
    eo_frequent_term_set = calculate_entropy_overlap(frequent_term_set, data)
    # print(eo_frequent_term_set)

    remove_document(eo_frequent_term_set)


if __name__ == "__main__":
    main()

