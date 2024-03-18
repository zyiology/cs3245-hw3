#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import string
import pickle
import os
import collections
import math

from nltk.corpus import reuters
from collections import Counter
from collections import defaultdict

# Format of dictionary {term: (offset, no_bytes, len_list), ...}
# Format of postings [(term, skipID), ...]

DOCUMENT_LENGTH_KEY = -100
TOTAL_DOCUMENTS_KEY = -200

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d temp_postings-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the temp_postings file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below
    file_ids = []
    temp_postings = defaultdict(list) 
    term_dictionary = {}
    doc_length_dictionary = {}
    stemmer = nltk.stem.PorterStemmer()
    total_documents = 0

    for fileid in os.listdir(in_dir): 
        file_ids.append(f"training/{fileid}")
        total_documents += 1
    # Creates out_postings file so that it can be read later
    file = open(out_postings, "wb")
    file.close()

    for fileid in file_ids: 
        words = reuters.words(fileid)
        words = [stemmer.stem(word).lower() for word in words if word not in string.punctuation] 
        word_count = Counter(words)
        id = int(fileid.split("/")[-1])
        # Create tuples of (docID, log term freqeuncy) and appending to temp_postings
        for word in word_count:
            temp_postings[word].append((id, 1 + math.log10(word_count[word])))
        # Document length calculation 
        sum = 0
        for word in word_count:
            sum += (1 + math.log10(word_count[word]))**2
        document_length = sum**0.5
        doc_length_dictionary[id] = document_length

    sorted_keys = sorted(list(temp_postings.keys()))   
    # Storing byte offset in dictionary so that postings lists can be retrieved without reading entire file
    current_offset = 0 
    with open(out_postings, "wb") as output:
        # Add document length dictionary
        dictionary_binary = pickle.dumps(doc_length_dictionary)
        no_of_bytes = len(dictionary_binary)
        term_dictionary[DOCUMENT_LENGTH_KEY] = (current_offset, no_of_bytes)
        output.write(dictionary_binary)
        current_offset += no_of_bytes
        for key in sorted_keys:
            to_add = sorted(temp_postings[key])
            to_add_binary = pickle.dumps(to_add)
            no_of_bytes = len(to_add_binary)
            term_dictionary[key] = (current_offset, no_of_bytes)
            output.write(to_add_binary)
            current_offset += no_of_bytes

    # Add total number of documents to dictionary
    term_dictionary[TOTAL_DOCUMENTS_KEY] = total_documents
    dictionary_binary = pickle.dumps(term_dictionary)
    with open(out_dict, "wb") as output:
        output.write(dictionary_binary)
    
    print ("indexing over")



# So this doesn't run when this file is imported in other scripts
if (__name__ == "__main__"): 
    input_directory = output_file_dictionary = output_file_postings = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-i': # input directory
            input_directory = a
        elif o == '-d': # temp_postings file
            output_file_dictionary = a
        elif o == '-p': # postings file
            output_file_postings = a
        else:
            assert False, "unhandled option"

    if input_directory == None or output_file_postings == None or output_file_dictionary == None:
        usage()
        sys.exit(2)

    build_index(input_directory, output_file_dictionary, output_file_postings)
    
'''
    with open("dictionary.txt","rb") as input:
        dictionary = pickle.loads(input.read())
    current_offset, no_of_bytes = dictionary["bahia"]
    with open("postings.txt", "rb") as input:
        input.seek(current_offset)
        posting = pickle.loads(input.read(no_of_bytes))
        print(posting)
    print(f"Total documents: {dictionary[TOTAL_DOCUMENTS_KEY]}")
'''
  



