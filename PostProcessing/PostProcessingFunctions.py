import os
import pandas as pd
from scipy import spatial
import scipy
def unzip_text_vectors(s3,bt_model,bucket):
    key = bt_model.model_data[bt_model.model_data.find("/", 5) + 1:]
    s3.Bucket(bucket).download_file(key, 'model.tar.gz')
    os.system("tar -xvf model.tar.gz")

def prepare_vectors_for_analysis(vector_file):
    vecs = pd.read_csv(vector_file)
    vecs = pd.DataFrame(vecs['118 100'].str.split().tolist())
    return vecs

def cosine_similarity_vector_comparison(vecs, word1, word2):
    #Grab the vector per word
    s1 = vecs[vecs[0] == word1]
    s2 = vecs[vecs[0] == word2]
    #Eliminate null values and the first column. The first column contains the word.
    s1 = pd.to_numeric(s1.iloc[0, 1:]).fillna(0)
    s2 = pd.to_numeric(s2.iloc[0, 1:]).fillna(0)
    #Calculate the cosine similarity
    cosine = scipy.spatial.distance.cosine(s1, s2)

    print('Word Embedding method with a cosine distance assesses that our two sentences are similar to',
          round((1 - cosine) * 100, 2), '%')
    return cosine