from collections import defaultdict, Counter
from typing import List
import concurrent.futures
import operator
import itertools
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
    # print(all_terms)
    
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
    print(common_words)
    
    return common_words

#unoptimised algorithm by eri
# def generate_frequent_term_set(common_words, data, min_support):
#     frequent_term_set = {}

#     # Count word occurrences in the documents
#     doc_word_freq = defaultdict(lambda: defaultdict(int))
#     for i, document in enumerate(data):
#         for word in document.split():
#             if word in common_words:
#                 doc_word_freq[i][word] += 1

#     # Generate combinations of words
#     for r in range(1, len(common_words) + 1):
#         word_combinations = combinations(common_words, r)

#         # Check minimum support for each combination
#         for combination in word_combinations:
#             support_documents = []
#             combination_freq = defaultdict(int)

#             # Update combination frequency by merging word frequencies from each document
#             for i, freq in doc_word_freq.items():
#                 if all(word in freq for word in combination):
#                     for word, count in freq.items():
#                         if word in combination:
#                             combination_freq[word] += count

#                     support_documents.append(f"D{i + 1}")

#             # If combination meets the minimum support, add it to frequent term set
#             if len(support_documents) >= min_support:
#                 frequent_term_set[", ".join(combination)] = (list(combination_freq.keys()), support_documents)

#     return frequent_term_set

#unoptimised algorithm by umar
# def generate_frequent_term_set(common_words, data, min_support):
#     frequent_term_set = {}

#     # Count word occurrences in the documents
#     doc_word_freq = {}
#     for i, document in enumerate(data):
#         doc_word_freq[i] = {}
#         for word in document.split():
#             if word in common_words:
#                 if not word in doc_word_freq[i]:
#                     doc_word_freq[i][word] = 1
#                 else:
#                     doc_word_freq[i][word] += 1

                    

#     # Generate combinations of words
#     for r in range(1, len(common_words) + 1):
#         word_combinations = combinations(common_words, r)

#         # Check minimum support for each combination
#         for combination in word_combinations:
#             support_documents = []
#             combination_freq = 0
            

#             for index_document, freq in doc_word_freq.items():
#                 all_combination_exists = True
#                 for haystack in combination:
#                     if not haystack in freq:
#                         all_combination_exists = False
#                 if all_combination_exists:
#                     support_documents.append(f"D{index_document+1}")
#                     combination_freq += 1
            

#             if combination_freq >= min_support:
#                 frequent_term_set[", ".join(combination)] = support_documents


#     return frequent_term_set

#optimised algorithm
def generate_frequent_term_set(common_words, data, min_support):
    frequent_term_set = {}
    counter = 0

    #print(common_words)
    
    # Count word occurrences in the documents
    doc_word_freq = {}
    for i, document in enumerate(data):
        temp = {}
        for word in document.split():
            if word in common_words:
                if not word in temp:
                    temp[word] = 1
                else:
                    temp[word] += 1
        if temp:
            doc_word_freq[i] = temp

    for i, (index_document, word_freq) in enumerate(doc_word_freq.items()):
        possible_word_combinations = set(word_freq)
        for r in range(1, len(possible_word_combinations) + 1):
            word_combinations = combinations(possible_word_combinations, r)


            for words in word_combinations:
                words = list(words)
                words.sort()
                combined_words = ", ".join(words)
                if not combined_words in frequent_term_set:
                    frequent_term_set[combined_words] = []

                frequent_term_set[combined_words].append(f"D{index_document+1}")

                for index_target in range(i+1, len(doc_word_freq)):
                    target_freqs = list(list(doc_word_freq.values())[index_target])
                    index_document_target = list(doc_word_freq.keys())[index_target]
                    if set(words).issubset(target_freqs):
                        frequent_term_set[combined_words].append(f"D{index_document_target+1}")
                    counter += 1

    frequent_term_set_temp = {}
    for word_combinations, freqs in frequent_term_set.items():
        if(len(freqs) >= min_support):
            frequent_term_set_temp[word_combinations] = list(set(freqs))

    print("Counter loop untuk menghitung possibilites : " + str(counter))
    print(frequent_term_set_temp)
    return frequent_term_set_temp


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

def remove_document(entropy_overlap_results, min_support):
    removed_docs = []
    lowest_dicts = []
    keys_to_remove = []
    lowest_value = float('inf')

    # Find the dict(s) with the lowest value
    for term_set, document in entropy_overlap_results.items():
        frequency = document[1]
        if frequency < lowest_value:
            lowest_value = frequency
            lowest_dicts = [{term_set: document}]
        elif frequency == lowest_value:
            lowest_dicts.append({term_set: document})

    # Get the list of documents to be removed from all lowest dicts
    for lowest_dict in lowest_dicts:
        removed_docs.extend(lowest_dict[list(lowest_dict.keys())[0]][0])
    # print("\nlowest dicts")
    # print(lowest_dicts)

    updated_results = {}
    for term_set, document in entropy_overlap_results.items():
        remaining_docs = [doc for doc in document[0] if doc not in removed_docs]
        if remaining_docs:
            updated_results[term_set] = (remaining_docs, document[1])

    for term_set, document in updated_results.items():
        if len(document[0]) < min_support:
            keys_to_remove.append(term_set)

    for key in keys_to_remove:
        del updated_results[key]
    
    return updated_results


    

def ftc(data, min_support):
    cluster = {}
    
    
    all_terms = generate_all_terms_flat(data)
    
    k_terms = find_common_words(all_terms, data, min_support)
    print(len(k_terms))
    print("Mengumpulkan k_terms...")
    # print(k_terms)
    
    frequent_term_set = generate_frequent_term_set(k_terms, data, min_support)
    print("membentuk frequent_term_set.....")
    print(frequent_term_set)
    # print(frequent_term_set)


    i = 0
    while len(frequent_term_set) > 1:
        print("Iterasi ke- " + str(i))
        eo_frequent_term_set = calculate_entropy_overlap(frequent_term_set, data)

        removed = remove_document(eo_frequent_term_set, min_support)

        # Use the frequent term set as the dictionary key for clustering
        for term_set, (documents, entropy_overlap) in eo_frequent_term_set.items():
            cluster[term_set] = (documents, entropy_overlap)

        frequent_term_set = {term_set: document[0] for term_set, document in removed.items()}
        i += 1


    return cluster


def main():
    min_support = 4
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

    cluster = ftc(data, min_support)
    # print(cluster)

    print("\nCluster:")
    for term_set, document in cluster.items():
        print(document[0], end=', ')

    print("\n\nDeksripsi cluster")
    for term_set, document in cluster.items():
        print(f"{{{''.join(term_set)}}}", end=", ")
        

if __name__ == "__main__":
    main()

