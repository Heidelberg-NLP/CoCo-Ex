CoCo-Ex is a tool for extracting concepts from texts and linking them to the ConceptNet knowledge graph, developed by Maria Becker, Katharina Korfhage and Anette Frank from the NLP Lab at Heidelberg University. 

CoCo-Ex extracts meaningful concepts from natural language texts and maps them to conjunct concept nodes in ConceptNet, utilizing the maximum of relational information stored in the ConceptNet knowledge graph. It takes into account the challenging characteristics of ConceptNet, namely that nodes are represented as non-canonicalized, free-form text. 

A commonly used shortcut for mapping phrases from natural language text to ConceptNet is to apply string matching, but given the non-normalized nature of the concepts in ConceptNet, this can result in an incomplete and noisy mapping, and a lot of relational knowledge in ConceptNet gets lost. Instead, CoCo-Ex enables the extraction of meaningful, important rather than overspecific or uninformative concepts, and allows to assess more relational information stored in the knowledge graph.

Check out our system demonstration video on Youtube: https://www.youtube.com/watch?v=bgqVhE2vR9A&feature=youtu.be

For questions or comments email us: mbecker@cl.uni-heidelberg.de

_____


CoCo-Ex is written in Python and requires the following software components:

- Python 3.6/3.7
- spacy 2.3.5
- nltk 3.5
- gensim 3.8.3
- pandas 1.2
- stanford parser 3.9.2

To extract entities with CoCo-Ex, run the following commands:

python CoCo-Ex_entity_extraction.py "path/to/inputfile.csv" "path/to/outputfile.tsv"

The system expects a .csv inputfile of the following format:

text_id;sent_1;sent_2;...;sent_n

Each text is one line, where the first column is the text_id and all other columns are one sentence per column.
If your inputfile has a different format, you will need to change the code snippet where it is parsed, at the bottom of the entity_extraction.py source code.

Note that you might need to set some more variables (such as the Stanford parser path, java path or embeddings path) as well, depending on your file structure.
These variables are currently hardcoded in the "main" section of the source code and can be changed accordingly there.

The output will be written to your specified outputpath as a .tsv file. It contains all the similarities calculated between each candidate node and each sentence's phrases.
Note that this file can take up a lot of memory for large inputs.

By default, the system will only calculate the length difference and dice similarity for a pair (the metrics we use in our paper), and fill the other possible similarity metrics with "None".
This is for performance reasons. However, this can be changed by a flag in the source code, if you wish to calculate other metrics as well.

To filter out overhead from the candidate nodes based on their similarities, execute the following command:

python CoCo-Ex_overhead_filter.py --inputfile "path/to/outputfile_of_first_step.tsv" --outputfile "path/to/new_outputfile.tsv" --len_diff_tokenlevel 1 --len_diff_charlevel 10 --dice_coefficient 0.85

The thresholds for the individual similarity metrics can be set as command line parameters as shown above (1/10/0.85 is our paper configuration).
The overhead filter currently only implements these three filters used in our paper. However, we will keep adding filters for the other similarity metrics to it in the future.

The file concepts_en_lemmas.p can be downloaded here: https://drive.google.com/file/d/107CE0Mn1TJST7sPu0h1ru1YvvUypqStw/view?usp=sharing

Feel free to contact us for any questions or issues!
