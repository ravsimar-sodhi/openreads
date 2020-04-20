import pandas as pd
import pickle
f=open("reco_model_cosine.pkl","rb")
cosine_sim=pickle.load(f)
f.close()
f=open("reco_model_indices.pkl","rb")
indices=pickle.load(f)
f.close()
df6=pd.read_csv("reco_df.csv",index_col="book_title")

def recommendations(title, cosine_sim = cosine_sim):
    
    recommended_books = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_10_indexes = list(score_series.iloc[1:11].index)
    for i in top_10_indexes:
        recommended_books.append(list(df6.index)[i])
    return recommended_books