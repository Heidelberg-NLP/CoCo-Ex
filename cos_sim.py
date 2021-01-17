import string
import numpy as np
from gensim.models import KeyedVectors
from scipy.spatial.distance import cosine

def cos_similarity(source_words, target_words, model, stops):
    #source_words = source.split(" ")
    #target_words = target.split(" ")

    vectors_to_compare = list()

    for words in [source_words, target_words]:

        #print(words)
        
        if len(words) > 1:
            joined_with_dashes = "_".join(words)
            #print("1")
            if joined_with_dashes in model:
                vector = model[joined_with_dashes]
                #print("2")
            else:
                #print("3")
                words_without_stops = [word for word in words if (word not in stops)]
                #print(words_without_stops)
                joined_with_dashes_nostops = "_".join(words_without_stops)
                if joined_with_dashes_nostops in model:
                    #print("4")
                    vector = model[joined_with_dashes_nostops]
                else:
                    #print("5")
                    vectors = [model[word] for word in words_without_stops if (word in model)]
                    if vectors:
                        #print("6")
                        vector = np.mean(vectors, axis=0)
                    else:
                        #print("7")
                        return 0.0
            
        else:
            try:
                vector = model[words[0]]
            except:
                return 0.0

        vectors_to_compare.append(vector)

        """
    if len(target_words) > 1:
        if "_".join(target_words) in model:
            target_vector = model["_".join(target_words)]
        else:
            target_vectors = [model[word] for word in target_words if word in model] # and word not in stops)]
            if target_vectors:
                target_vector = np.mean(target_vectors, axis=0)
            else:
                return 0.0
    else:
        try:
            target_vector = model[target_words[0]]
        except:
            return 0.0
        """
    return 1 - cosine(vectors_to_compare[0], vectors_to_compare[1])
    

if __name__ == "__main__":
    embeddings_path = 'GoogleNews-vectors-negative300.bin'
    #embeddings_path = "numberbatch-en-17.06.txt"
    model = KeyedVectors.load_word2vec_format(embeddings_path, binary=False)

    with open('stopwords.txt', 'r') as f:
        stops = set(line.strip() for line in f.readlines())
    stops = stops.union(string.punctuation)


    print(cos_similarity(["make", "you", "sneeze"], ["separate"], model, stops))

