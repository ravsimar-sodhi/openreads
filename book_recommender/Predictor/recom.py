from django.shortcuts import render
from django.conf import settings
import pandas as pd
import pickle
import os
path = os.path.join(settings.MODELS, 'reco_model_cosine_small.pkl')
f = open(path,"rb")
print(path)
cosine_sim=pickle.load(f)
f.close()
path = os.path.join(settings.MODELS, 'reco_model_indices.pkl')
f=open(path,"rb")
print(path)
indices=pickle.load(f)
f.close()
path = os.path.join(settings.MODELS, 'reco_df.csv')
print(path)
df6=pd.read_csv(path,index_col="book_title")

def recommendations(title, cosine_sim = cosine_sim):
    
    recommended_books = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indexes = list(score_series.iloc[1:11].index)
    for i in top_10_indexes:
        recommended_books.append(list(df6.index)[i])
    return recommended_books
