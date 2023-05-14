import math

def document_pivot(cluster):
    # Get the number of documents in the cluster
    num_documents = len(cluster[1])

    # Get the number of words in the cluster
    num_words = len(cluster[0])

    # Get the average document length
    avg_document_length = num_words / num_documents

    # Get the probability of each word in the cluster
    p = [cluster[1].count(word) / avg_document_length for word in cluster[0]]

    # Get the relevance of each word to the cluster
    r = [cluster[1].count(word) / len(cluster[1]) for word in cluster[0]]

    # Calculate the pivot
    pivot = sum(p * r) / sum(p)

    # Get the score of the cluster
    score = math.exp(pivot)

    return score

def main():
    clusters = [
    ('banjir', ['D5', 'D8', 'D15', 'D17']),
    ('dpr', ['D5', 'D8', 'D15', 'D16']),
    ('anies', ['D5', 'D8', 'D15', 'D16', 'D17']),
    ('anies', 'banjir', ['D5', 'D8', 'D15', 'D17']),
    ('anies', 'dpr', ['D5', 'D8', 'D15', 'D16']),
]
    document_pivot(clusters)

    for cluster in clusters:
        print(cluster[0], document_pivot(cluster))



if __name__ == "__main__":
    main()