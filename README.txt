This is the README file for A0216276A's, A0291640H's submission
Email(s): e0538377@u.nus.edu, e1332814@u.nus.edu

== Python Version ==

We're using Python Version 3.11.2 for this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

The Reuters corpus was accessed via API with reuters.raw() and tokenized with word_tokenize(), with punctuation then removed and the remaining text stemmed and case-folded. Search terms for reuters.raw() are the file names in the specified in_dir appended to "training" since it was specified that we would be using the training set only e.g. "training/1".

build_index() in index.py hashes terms and postings lists of [(docID, log term frequency), ...] into the temporary postings dictionary in memory, which is then written to disk as postings.txt once all files in the input directory have been processed. 2 files are outputted: dictionary.txt, with a dictionary of (term, (byte offset of posting list in postings.txt, number of bytes of postings list)), and postings.txt, as previously mentioned, both serialised with Pickle. The byte offset approach ensures that postings lists can be read in search.py without reading the entire postings.txt. A dictionary of document vector lengths for all documents, as well as a variable for the total number of documents, are also added into dictionary.txt with unique keys to allow for calculations in the search process.

For search:
QueryProcessor class is defined in query_processor.py, handles an individual query using the process_query() method. Query is processed as follows: word_tokenize() -> remove punctuation -> remove duplicate terms -> lower() -> stem()
invalid terms (i.e. not defined in dictionary in indexing) are removed. postings list for each term are retrieved, used to calculate scores following algorithm in lecture notes
top 10 highest scores are retrieved in sorted order, then documents with equal scores are sorted by document number.

search.py handles the processing of the query and output file.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

index.py: Code for indexing logic.
search.py: Code for search logic. 
query_processor.py: Helper class for processing search. 
dictionary.txt: Dictionary serialised with Pickle. 
postings.txt: Posting lists serialised with Pickle.

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[ X ] We, A0216276A and A0291640H, certify that we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, we
expressly vow that we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

https://www.geeksforgeeks.org/defaultdict-in-python/ - functionality for defaultdict to facilitate indexing logic, since new terms are often indexed
