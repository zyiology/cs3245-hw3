#!/usr/bin/python3
import re
import nltk
import sys
import getopt
from collections import defaultdict
from math import log
import heapq

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below

    with open(query_file, 'r') as f:
        queries = f.readlines()  

    result_strings = []
    for q in queries:
        result_strings.append(process_query(q))
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(result_strings))
    
    print(f'output written to {output_file}')


def process_query(query):
    number_results = 10
    scores = defaultdict(float)

    query_terms = set(query.split()) # remove duplicate terms

    N = 1000 # TODO retrieve from index
    log_N = log(N)

    for term in query_terms:
        postings_list = fetch_postings_list(term)

        # calculate tf.idf for this term
        # heuristic: assume log freq weight of term t in query = 1
        docu_freq = len(postings_list)
        weight_term = log_N - log(docu_freq)

        for (doc_id, term_freq) in postings_list:
            # compute tf.idf for term in document
            weight_docu = (1 + log(term_freq))
            scores[doc_id] += weight_term * weight_docu

    for doc_id in scores.keys():
        scores[doc_id] /= get_document_length(doc_id)

    highest_scores = heapq.nlargest(number_results, scores.items(), key=lambda item: item[1])
    highest_keys = [item[0] for item in highest_scores]

    return ",".join(highest_keys)

# TODO
def fetch_postings_list(term):
    return

def get_document_length(doc_id):
    return

dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
