import random
from collections import Counter
import nltk


class LDA(object):
    '''
    Latent Dirichlet Allocation (LDA), a topic model designed for text documents.

    Topic models extract the key concepts in a set of documents. 
    Each concept can be described by a list of keywords from most to least important. 
    Then, each document can be connected to those concepts, or topics, to determine
    how representative that document is of that overall concept.
    '''

    def __init__(self, K, max_iteration):
        self.K = K
        self.max_iteration = max_iteration

    def sample_from_weights(self, weights):
        '''
        This function randomly choose an index based on an arbitrary set of weights.
        Return the first weight's index that is greater than or equal to a random number.
        '''
        total = sum(weights)
        rnd = total * random.random()  # uniform between 0 and total
        for i, w in enumerate(weights):
            rnd -= w  # return the smallest i such that
            if rnd <= 0:
                return i  # sum(weights[:(i+1)]) >= rnd

    def p_topic_given_document(self, topic, d, alpha=0.1):
        '''
        P(topic|d,Alpha)
        The fraction of words in document d
        that are assigned to topic (plus some smoothing)
        '''
        return ((self.document_topic_counts[d][topic] + alpha) /
                (self.document_lengths[d] + self.K * alpha))

    def p_word_given_topic(self, word, topic, beta=0.1):
        '''
        P(word|topic,Beta)
        The fraction of words assigned to topic
        that equal word (plus some smoothing)
        '''
        return ((self.topic_word_counts[topic][word] + beta) /
                (self.topic_counts[topic] + self.W * beta))

    def topic_weight(self, d, word, topic):
        '''
        P(topic|word,Alpha,Beta) = P(topic|d,Alpha) * P(word|topic,Beta)
        Given a document and a word in that document,
        return the weight for the k-th topic
        '''
        return self.p_word_given_topic(word, topic) * self.p_topic_given_document(topic, d)

    def choose_new_topic(self, d, word):
        return self.sample_from_weights([self.topic_weight(d, word, k)
                                         for k in range(self.K)])

    def gibbs_sample(self, document_topics):
        '''
        Gibbs sampling https://en.wikipedia.org/wiki/Gibbs_sampling.
        '''
        for _ in range(self.max_iteration):
            for d in range(self.D):
                for i, (word, topic) in enumerate(zip(self.documents[d],
                                                      document_topics[d])):
                    # remove this word / topic from the counts
                    # so that it doesn't influence the weights
                    self.document_topic_counts[d][topic] -= 1
                    self.topic_word_counts[topic][word] -= 1
                    self.topic_counts[topic] -= 1
                    self.document_lengths[d] -= 1

                    # choose a new topic based on the weights
                    new_topic = self.choose_new_topic(d, word)
                    document_topics[d][i] = new_topic

                    # and now add it back to the counts
                    self.document_topic_counts[d][new_topic] += 1
                    self.topic_word_counts[new_topic][word] += 1
                    self.topic_counts[new_topic] += 1
                    self.document_lengths[d] += 1

    def run(self, documents):
        # How many times each topic is assigned to each document.
        self.document_topic_counts = [Counter()
                                      for _ in documents]
        # How many times each word is assigned to each topic.
        self.topic_word_counts = [Counter() for _ in range(self.K)]
        # The total number of words assigned to each topic.
        self.topic_counts = [0 for _ in range(self.K)]
        # The total number of words contained in each document.
        self.document_lengths = [len(d) for d in documents]
        self.distinct_words = set(
            word for document in documents for word in document)
        # The number of distinct words
        self.W = len(self.distinct_words)
        # The number of documents
        self.D = len(documents)
        # document_topics is a Collection that assign a topic (number between 0 and K-1) to each word in each document.
        # For example: document_topic[3][4] -> [4 document][id of topic assigned to 5 word]
        # This collection defines each document's distribution over topics, and
        # implicitly defines each topic's distribution over words.
        document_topics = [[random.randrange(self.K) for _ in document]
                           for document in documents]

        self.documents = documents  # Store the pre-processed documents

        for d in range(self.D):
            for word, topic in zip(self.documents[d], document_topics[d]):
                self.document_topic_counts[d][topic] += 1
                self.topic_word_counts[topic][word] += 1
                self.topic_counts[topic] += 1

        self.gibbs_sample(document_topics)

        return (self.topic_word_counts, self.document_topic_counts)

    def get_topic_word_list(self):
        topic_word_list = {}
        for topic in range(self.K):
            data = []
            for word, count in self.topic_word_counts[topic].most_common():
                if count > 1:
                    data.append(word)
            topic_word_list[f"Topic {topic+1}"] = data
        return topic_word_list
