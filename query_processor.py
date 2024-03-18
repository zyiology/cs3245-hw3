import pickle
import heapq
from collections import defaultdict
from math import log
from index import DOCUMENT_LENGTH_KEY, TOTAL_DOCUMENTS_KEY
from nltk import PorterStemmer, word_tokenize
from string import punctuation

class QueryProcessor:

    def __init__(self, dictionary_file, postings_file):
        with open(dictionary_file, 'rb') as f:
            self.dictionary = pickle.load(f)

        with open(postings_file, 'rb') as f:
            offset, bytes_to_read = self.dictionary[DOCUMENT_LENGTH_KEY]
            f.seek(offset)
            self.document_length_dictionary = pickle.loads(f.read(bytes_to_read))

        self.postings_file = postings_file

        self.stemmer = PorterStemmer()

    
    def process_query(self, query, number_results=10):
        scores = defaultdict(float)

        # tokenize and remove punctuation
        query_terms = word_tokenize(query)
        query_terms = [term for term in query_terms if term not in punctuation]

        # remove duplicate terms and stem the terms
        query_terms = set(query_terms)
        query_terms = [self.stemmer.stem(term.lower()) for term in query_terms]

        # remove invalid terms
        query_terms = [term for term in query_terms if term in self.dictionary]

        log_N = log(self.dictionary[TOTAL_DOCUMENTS_KEY])

        for term in query_terms:
            postings_list = self.fetch_postings_list(term)

            # calculate tf.idf for this term
            # heuristic: assume log freq weight of term t in query = 1
            docu_freq = len(postings_list)
            weight_term = log_N - log(docu_freq)

            for (doc_id, weight_docu) in postings_list:
                # compute tf.idf for term in document
                # weight_docu = (1 + log(term_freq))
                scores[doc_id] += weight_term * weight_docu

        for doc_id in scores.keys():
            scores[doc_id] /= self.document_length_dictionary[doc_id]

        if len(scores) == 0:
            return ""

        highest_scores = heapq.nlargest(number_results, scores.items(), key=lambda item: item[1])

        # order by scores, then by term

        highest_terms = []
        same_scores = []
        for item in highest_scores:
            # if score is the same as the previous highest score, add to list
            if highest_terms and item[1] == highest_terms[-1][1]:
                same_scores.append(item)
            # if score is different, sort the list of same scores by term
            elif same_scores:
                same_scores.sort(key=lambda x: x[0])
                highest_terms.extend(same_scores)
            else:
                highest_terms.append(item)
        
        highest_terms = [str(item[0]) for item in highest_terms]

        return " ".join(highest_terms)
    

    def fetch_postings_list(self, term):
        offset, bytes_to_read = self.dictionary[term]

        # read the postings list from the postings file
        with open(self.postings_file, 'rb') as f:
            f.seek(offset)
            postings_list = pickle.loads(f.read(bytes_to_read))

        return postings_list
    
